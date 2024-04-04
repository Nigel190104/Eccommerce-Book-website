from django.test import TestCase

from store.models import Category, Product, User
from django.urls import reverse

class TestCategoriesModel(TestCase):
    #the creation of data which we want to test against
    #we are making sure that the name and slug match
    #we mainly want to focus on testing the logic that we create
    def setUp(self):
        self.data1 = Category.objects.create(name ='django', slug='django')
    
    def test_category_model_entry(self):
        """
        Test category model data insertion/types/field attributes
        """
        data = self.data1
        #isinstance is going to take the data and it is going to be tested against my model
        #if it is the corrert data then it will return true
        #so depending on what your expected values for the model and the specific data that 
        #is going to be associated with it you decide the type of assert is necessary in
        #order to test functionaity
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')

    def test_category_model_entry(self):
        """
        Test category model alug and URL reverse
        """
        data = self.data1 
        response = self.client.post(reverse('store:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        #although in our initial models we do not have a create_by_id and category-id field but in the store produc table django automatically created one for me
        #so thats what we are referencing
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1, slug='django-beginners', price='20.00', image='django')
        self.data2 = Product.objects.create(category_id=1, title='django advanced', created_by_id=1, slug='django-advanced', price='20.00', image='django', is_active=False)

    def test_products_model_entry(self):
        """
        Test product model data isneriton/types/fields attributes
        """

        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')

    def test_products_url(self):
        """
        Test product mdoel slug and URL reverse
        """

        data = self.data1
        url = reverse('store:product_detail', args=[data.slug])
        self.assertEqual(url, '/django-beginners')
        response = self.client.post(reverse('store:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_products_custom_manager_basic(self):
        """
        Test product manager return only active products
        """
        data = Product.products.all()
        self.assertEqual(data.count(), 1)
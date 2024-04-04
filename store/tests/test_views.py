#this is the way in which we should formatt our imports in files
#python libaries
from unittest import skip

from django.contrib.auth.models import User
#django resources
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
#our program resources specific to this project
from store.views import all_products

# this skipping of tests is useful when changes
# have been made to the specific file in which
# you are testing the values gotten and you are
# yet to update the test being performed to accomodate this change
@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django beginners',
                                created_by_id=1,
                                slug='django-beginners',
                                price='20.00', image='django')

    #this approach involves simulating the browser and then returning the data from the program as
    #if we were runnning the browser
    #not the best way to test the functionality of the code
    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        #this is making sure that the request made has succeded which is denoted by 200
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)
#we want to similate via tests a user accessing our views    
    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test category response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        print(html)
        #this akin to sayin the text within the speechmarks should be located in the html file
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    #testimg via request factory allows us to test the website as a
    #use to look for specific functionality within your views that you want to test
    def test_view_function(self):
        request = self.factory.get('/django-beginners')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

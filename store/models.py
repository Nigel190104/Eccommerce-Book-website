from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

#the are the isntrucntion for django or templates for django in order to create our tables in the database
#this is done by describing the tables in a class in order to build them
#these models/classes
# Create your models here.

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
#we are building a shop so we need some tables for our products
#we also need to consider how we are going to manage those products
#the category table will record the categories that we have in our shop for our products
#then we will will record our products table
#then connect our products table to our category table
##we want to be bale ot define the category wihtin our product
#we are extending from models which is going to procide us access to the functionality that we're going  to need to build a model
#and describe a model
#our category we need to record the name
class Category(models.Model):
    #we are going to be typing characters inside this field
    name = models.CharField(max_length = 255, db_index=True)
    #this allow us to be able to access the category via typing into the browser the name of the category
    #e.g. 127.0.0.1;800/django/
    #the above line will allow us to access all the items in the category
    #it will be behind the scenes describing what should be inside this field
    #the unique equals true make sure that we dont have more than one of the same type of category
    #as well as makes sure that special characters cant be sued
    slug = models.SlugField(max_length = 255, unique=True)
    #this is jsut making sure that it sets the plural name of the Category model to categories and not Category's 
    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])
    
    def __str__(self):
        return self.name

class Product(models.Model):
    #this establishes a link between the categories and the product table
    #if we do not have a category therfore by implication we can not have a produt
    #so the field category has to be populated at all times
    #so if no category exists we will have to delete all products associated with that specific category
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    #for the product added we want to record who made that data
    #this references the django default user table and builds a connection to it
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'product_creator')

    title = models.CharField(max_length =255)

    author = models.CharField(max_length =255, default='admin')
    #no length specified since this field in particular will be long
    description = models.TextField(blank = True)
    #we are storing the link to the image in the databse and not the image itself
    #there is apackage that we install called pillows which allows for the manging of images
    image = models.ImageField(upload_to='images/', default='images/arrows.png')
    #this will be used to present the individual item on the page
    slug = models.SlugField(max_length = 255) 
    price = models.DecimalField(max_digits=4, decimal_places=2)
    #might need to add some point if not covered in the video look at finding ways to automate
    #the is_active field such that wen stokc value or rather there is no longer any stokc for that particular product we then 
    #make the product incative setting the value to false implying it can no longer be bought
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)
    #triggered everytime we make an update to the product changing one of its fields etc.
    updated = models.DateTimeField(auto_now = True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'products'
        #specify the order we want the fields for the product to be in
        #we want to order the products such that the last item to be added is shown first
        #so in descenging order
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    
    def __str__(self):
        return self.title
from django.urls import path

from . import views

#provides a quick reference to the url in this file
app_name = 'store'

urlpatterns = [
    #this is connecting a view or currently unbuilt path to the root path(homepage)
    path('', views.all_products, name='all_products'),
    #the slug here refers to the data type that we are trying to store
    #the secong slug refers to dat
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
]

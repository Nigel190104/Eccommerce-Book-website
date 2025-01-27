from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def all_products(request):
    #runs a query on the Product table and retrieves all the data
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/single.html', {'product':product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category':category, 'products':product})

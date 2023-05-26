from typing import Any
from django.views.generic import ListView
from django.shortcuts import render
from vendor.models import Product

def fetch_products(category):
    if category == 'all':
        return Product.objects.all()
    
    return Product.objects.filter(category=category)

def home_page(req):
    products = Product.objects.all()[0:10]
    return render(req, "website/index.html", {"products": products})


def cart_page(req):
    return render(req, "website/cart.html")

class Shop_Page(ListView):
    model = Product
    template_name = "website/shop.html"
    context_object_name = 'products'
    paginate_by = 18
    
    
    def get_queryset(self):
        category = self.kwargs["category"]
        products = fetch_products(category)
        return products


def contact_page(req):
    return render(req, "website/contact.html")

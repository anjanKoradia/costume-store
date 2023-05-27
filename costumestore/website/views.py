from django.views.generic import ListView, DetailView
from django.shortcuts import render
from vendor.models import Product
import random


def fetch_products(category):
    if category == "all":
        return Product.objects.all()

    return Product.objects.filter(category=category)


def home_page(req):
    products = Product.objects.all()[0:10]
    return render(req, "website/index.html", {"products": products})


def cart_page(req):
    return render(req, "website/cart.html")


def product_details(req, id):
    product_details = Product.objects.get(id=id)
    related_products = Product.objects.filter(
        category=product_details.category, subcategory=product_details.subcategory
    )

    random_related_products = random.sample(list(related_products), 8)

    return render(
        req,
        "website/product-details.html",
        {
            "product_details": product_details,
            "related_products": random_related_products,
        },
    )


def contact_page(req):
    return render(req, "website/contact.html")


class Shop_Page(ListView):
    model = Product
    template_name = "website/shop.html"
    context_object_name = "products"
    paginate_by = 18

    def get_queryset(self):
        category = self.kwargs["category"]
        products = fetch_products(category)
        return products

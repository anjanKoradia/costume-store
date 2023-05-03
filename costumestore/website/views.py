from django.shortcuts import render
from django.contrib.auth import logout


def home_page(req):
    return render(req, "website/index.html")


def cart_page(req):
    return render(req, "website/cart.html")


def shop_page(req):
    return render(req, "website/shop.html")


def contact_page(req):
    return render(req, "website/contact.html")

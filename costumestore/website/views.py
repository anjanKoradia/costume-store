from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import CartItem, Cart
from vendor.models import Product
from .forms import CartItemForm
import random
import uuid


def home_page(req):
    products = Product.objects.all()[0:10]
    return render(
        req,
        "website/index.html",
        {"products": products},
    )


class Cart_Operations:
    @staticmethod
    def cart_page(req):
        cart_items = CartItem.objects.filter(cart__user=req.user)
        return render(req, "website/cart.html", {"cart_items": cart_items})

    @staticmethod
    def add_to_cart(req, id):
        form = CartItemForm(req.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            return render(
                req,
                "website/product-details.html",
                {"product_details": Product.objects.get(id=id), "errors": errors},
            )

        data = form.cleaned_data

        product = get_object_or_404(Product, id=id)
        cart, created = Cart.objects.get_or_create(user=req.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            quantity=data["quantity"],
            size=data["size"],
            color=data["color"],
        )

        if not item_created:
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        return redirect("home_page")

    @staticmethod
    def decrease_cart_item_qty(req, id):
        cart_item = CartItem.objects.get(id=id)
        cart_item.quantity = cart_item.quantity - 1
        cart_item.save()

        return redirect("cart_page")

    @staticmethod
    def increase_cart_item_qty(req, id):
        cart_item = CartItem.objects.get(id=id)
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()

        return redirect("cart_page")


def contact_page(req):
    return render(req, "website/contact.html")


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


class Shop_Page(ListView):
    model = Product
    template_name = "website/shop.html"
    context_object_name = "products"
    paginate_by = 18

    def get_queryset(self):
        category = self.kwargs["category"]
        if category == "all":
            return Product.objects.all()

        return Product.objects.filter(category=category)

from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart, Wishlist, WishlistItem
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from vendor.models import Product
from .forms import CartItemForm
import random


def home_page(req):
    products = Product.objects.all()[0:10]
    wishlist = []
    wishlist_product_id = []

    if req.user.is_authenticated:
        wishlist_product_id = WishlistItem.objects.filter(
            wishlist__user=req.user
        ).values_list("product", flat=True)

        wishlist = WishlistItem.objects.filter(wishlist__user=req.user)

    return render(
        req,
        "website/index.html",
        {
            "products": products,
            "wishlist_product_id": wishlist_product_id,
            "wishlist": wishlist,
            "total_price": Wishlist.objects.get(user=req.user).total_price,
        },
    )


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


class Wishlist_Operations:
    @staticmethod
    def add(req, id):
        product = Product.objects.get(id=id)
        wishlist, created = Wishlist.objects.get_or_create(user=req.user)

        wishlist_item, item_created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )

        if wishlist_item:
            wishlist.total_price = wishlist.total_price + wishlist_item.product.price
            wishlist.save()

        referring_url = req.META.get("HTTP_REFERER")
        return redirect(referring_url)

    @staticmethod
    def remove(req, id):
        wishlist_item = WishlistItem.objects.get(product__id=id)

        wishlist = Wishlist.objects.get(user=req.user)
        wishlist.total_price = wishlist.total_price - wishlist_item.product.price
        wishlist.save()

        wishlist_item.delete()

        referring_url = req.META.get("HTTP_REFERER")
        return redirect(referring_url)


class Cart_Operations:
    @staticmethod
    @login_required
    def cart_page(req):
        cart = Cart.objects.get(user=req.user)
        cart_items = CartItem.objects.filter(cart__user=req.user)
        
        return render(req, "website/cart.html", {"cart_items": cart_items, "cart_total_price": cart.total_price })

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
            size=data["size"],
            color=data["color"],
            defaults={
                "quantity": data["quantity"],
            },
        )

        cart.total_price = cart.total_price + cart_item.product.price
        cart.save()

        if not item_created:
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        return redirect("home_page")

    @staticmethod
    def decrease_cart_item_qty(req, id):
        cart = Cart.objects.get(user=req.user)
        cart_item = CartItem.objects.get(id=id)
        
        cart.total_price = cart.total_price - cart_item.product.price
        cart.save()
        
        cart_item.quantity = cart_item.quantity - 1
        cart_item.save()

        return redirect("cart_page")

    @staticmethod
    def increase_cart_item_qty(req, id):
        cart = Cart.objects.get(user=req.user)
        cart_item = CartItem.objects.get(id=id)
        
        cart.total_price = cart.total_price + cart_item.product.price
        cart.save()
        
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()

        return redirect("cart_page")


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

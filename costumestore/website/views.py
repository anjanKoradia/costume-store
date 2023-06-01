from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart, Wishlist, WishlistItem
from django.views.generic import ListView
from vendor.models import Product
from .forms import CartItemForm
import random


def home_page(request):
    products = Product.objects.all()[0:10]
    wishlist = []
    wishlist_product_id = []
    total_price = 0
    
    if request.user.is_authenticated and request.user.role == "customer":
        wishlist_product_id = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).values_list("product", flat=True)

        wishlist = WishlistItem.objects.filter(wishlist__user=request.user)
        total_price = Wishlist.objects.get(user=request.user).total_price
        
    return render(
        request,
        "website/index.html",
        {
            "products": products,
            "wishlist_product_id": wishlist_product_id,
            "wishlist": wishlist,
            "total_price": total_price,
        },
    )


def contact_page(request):
    return render(request, "website/contact.html")


def product_details(request, id):
    wishlist_product_id = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).values_list("product", flat=True)

        
    product_details = Product.objects.get(id=id)
    related_products = Product.objects.filter(
        category=product_details.category, subcategory=product_details.subcategory
    )

    random_related_products = random.sample(list(related_products), 8)

    return render(
        request,
        "website/product-details.html",
        {
            "product_details": product_details,
            "wishlist_product_id": wishlist_product_id,
            "related_products": random_related_products,
        },
    )


class Wishlist_Operations:
    def add(request, id):
        product = Product.objects.get(id=id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        wishlist_item, item_created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, product=product
        )

        if wishlist_item:
            wishlist.total_price = wishlist.total_price + wishlist_item.product.price
            wishlist.save()

        referring_url = request.META.get("HTTP_REFERER")
        return redirect(referring_url)

    def remove(request, id):
        wishlist_item = WishlistItem.objects.get(product__id=id)

        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.total_price = wishlist.total_price - wishlist_item.product.price
        wishlist.save()

        wishlist_item.delete()

        referring_url = request.META.get("HTTP_REFERER")
        return redirect(referring_url)


class Cart_Operations:
    def cart_page(request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart__user=request.user)

        return render(
            request,
            "website/cart.html",
            {"cart_items": cart_items, "cart_total_price": cart.total_price},
        )

    def add_to_cart(request, id):
        form = CartItemForm(request.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            return render(
                request,
                "website/product-details.html",
                {"product_details": Product.objects.get(id=id), "errors": errors},
            )

        data = form.cleaned_data

        product = get_object_or_404(Product, id=id)
        cart, created = Cart.objects.get_or_create(user=request.user)

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

    def decrease_cart_item_qty(request, id):
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(id=id)

        cart.total_price = cart.total_price - cart_item.product.price
        cart.save()

        cart_item.quantity = cart_item.quantity - 1
        cart_item.save()

        return redirect("cart_page")

    def increase_cart_item_qty(request, id):
        cart = Cart.objects.get(user=request.user)
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

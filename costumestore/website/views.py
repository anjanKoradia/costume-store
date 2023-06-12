from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart, Wishlist, WishlistItem
from django.views.generic import ListView
from vendor.models import Product
from .forms import CartItemForm
import random
from payment.models import OrderItem


def home_page(request):
    products = Product.objects.all()
    random_products = random.sample(list(products), 10)
    wishlist_products = []

    if request.user.is_authenticated and request.user.role == "customer":
        wishlist_products = filter(
            lambda product: product.wishlist_item.filter(wishlist__user=request.user),
            random_products,
        )

    return render(
        request,
        "website/index.html",
        {
            "products": random_products,
            "wishlist_products": list(wishlist_products),
        },
    )


def contact_page(request):
    return render(request, "website/contact.html")


def my_orders(request):
    ordered_items = OrderItem.objects.filter(order__user=request.user)
    return render(request, "website/orders.html", {"ordered_items": ordered_items})


def product_details(request, id):
    product_details = Product.objects.get(id=id)
    print(product_details.vendor.user)

    related_products = Product.objects.filter(
        category=product_details.category, subcategory=product_details.subcategory
    )
    random_related_products = random.sample(list(related_products), 4)

    in_wishlist = False

    if request.user.is_authenticated and request.user.role == "customer":
        in_wishlist = product_details.wishlist_item.filter(wishlist__user=request.user)

    return render(
        request,
        "website/product-details.html",
        {
            "product_details": product_details,
            "in_wishlist": in_wishlist,
            "related_products": random_related_products,
        },
    )


class Wishlist_Operations:
    def wishlist_page(request):
        wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user)
        return render(
            request, "website/wishlist.html", {"wishlist_items": wishlist_items}
        )

    def wishlist_operations(request, operation, id):
        if operation == "add":
            product = Product.objects.get(id=id)
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)

            wishlist_item, item_created = WishlistItem.objects.get_or_create(
                wishlist=wishlist, product=product
            )

            if wishlist_item:
                wishlist.total_price = (
                    wishlist.total_price + wishlist_item.product.price
                )
                wishlist.save()

        elif operation == "remove":
            WishlistItem.objects.get(product__id=id).delete()

        referring_url = request.META.get("HTTP_REFERER")
        return redirect(referring_url)


class Cart_Operations:
    def cart_page(request):
        cart_items = CartItem.objects.filter(cart__user=request.user)

        return render(request, "website/cart.html", {"cart_items": cart_items})

    def add_to_cart(request, id):
        form = CartItemForm(request.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            print(errors)
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

        cart.total_price = cart.total_price + (
            cart_item.product.price * cart_item.quantity
        )
        cart.save()

        if not item_created:
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        return redirect("cart_page")

    def cart_item_qty(request, operation, id):
        cart_item = CartItem.objects.get(id=id)
        cart = cart_item.cart

        if operation == "increase":
            cart.total_price = cart.total_price + cart_item.product.price
            cart.save()

            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        elif operation == "decrease":
            cart.total_price = cart.total_price - cart_item.product.price
            cart.save()

            cart_item.quantity = cart_item.quantity - 1
            cart_item.save()

        elif operation == "delete":
            cart_item.delete()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.paginate_queryset(self.get_queryset(), self.paginate_by)[2]
        wishlist_products = []

        if self.request.user.is_authenticated and self.request.user.role == "customer":
            wishlist_products = filter(
                lambda product: product.wishlist_item.filter(
                    wishlist__user=self.request.user
                ),
                products,
            )

        context["wishlist_products"] = list(wishlist_products)
        context["category"] = self.kwargs["category"]
        return context

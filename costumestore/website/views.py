import random
import json
from django.http import JsonResponse
from django.db.models import Min, Max
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, View, DetailView
from costumestore.services import HandelErrors
from payment.models import OrderItem
from vendor.models import Product, Color, Size
from .models import CartItem, Cart, Wishlist, WishlistItem
from .forms import CartItemForm


class HomePage(ListView):
    model = Product
    template_name = "website/index.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_products = []

        if self.request.user.is_authenticated and self.request.user.role == "customer":
            wishlist_products = filter(
                lambda product: product.wishlist_items.filter(
                    wishlist__user=self.request.user
                ),
                context["object_list"],
            )

        context["wishlist_products"] = wishlist_products
        return context


def contact_page(request):
    """
    Render the contact page.

    Renders the 'website/contact.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    return render(request, "website/contact.html")


class MyOrders(ListView):
    model = OrderItem
    template_name = "website/orders.html"
    context_object_name = "ordered_items"
    paginate_by = 10

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)


class ProductDetails(DetailView):
    model = Product
    template_name = "website/product-details.html"
    context_object_name = "product_details"
    slug_url_kwarg = "id"
    slug_field = "id"
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_details = context["object"]

        related_products = Product.objects.filter(
            category=product_details.category, subcategory=product_details.subcategory
        )
        random_related_products = random.sample(list(related_products), 4)

        in_wishlist = False

        if self.request.user.is_authenticated and self.request.user.role == "customer":
            in_wishlist = product_details.wishlist_items.filter(
                wishlist__user=self.request.user
            )

        context["related_products"] = random_related_products
        context["in_wishlist"] = in_wishlist
        return context


class WishlistOperations(View):
    def get(self, request):
        wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user)
        return render(
            request, "website/wishlist.html", {"wishlist_items": wishlist_items}
        )

    def post(self, request):
        data = json.loads(request.body)
        operation = data.get("operation")
        id = data.get("id")

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

            return JsonResponse(
                {
                    "message": "Added to wishlist",
                    "items_count": wishlist.wishlist_items.all().count(),
                }
            )

        if operation == "remove":
            wishlist_item = WishlistItem.objects.get(product__id=id).delete()
            items_count = WishlistItem.objects.filter(
                wishlist__user=request.user
            ).count()
            return JsonResponse(
                {"message": "Removed from wishlist", "items_count": items_count}
            )


class CartOperations(View):
    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        return render(request, "website/cart.html", {"cart_items": cart_items})

    def post(self, request):
        id = request.POST.get("id")
        form = CartItemForm(request.POST)

        if not form.is_valid():
            errors = HandelErrors.form_errors(form.errors, "list")
            return JsonResponse(errors, status=400, safe=False)

        data = form.cleaned_data

        product = Product.objects.get(id=id)
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

        return JsonResponse(
            {"message": "Added to cart successfully", "redirect_url": reverse("cart")},
            status=201,
        )

    def patch(self, request):
        data = json.loads(request.body)

        operation = data.get("operation")
        id = data.get("id")

        cart_item = CartItem.objects.get(id=id)
        cart = cart_item.cart

        if operation == "increase":
            cart.total_price = cart.total_price + cart_item.product.price
            cart.save()

            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()

        if operation == "decrease":
            cart.total_price = cart.total_price - cart_item.product.price
            cart.save()

            cart_item.quantity = cart_item.quantity - 1
            cart_item.save()

        if operation == "delete":
            cart_item.delete()

        cart_count = cart.cart_items.count()

        return JsonResponse(
            {
                "quantity": cart_item.quantity,
                "item_price": cart_item.product.price,
                "total_price": cart_item.cart.total_price,
                "cart_count": cart_count,
            }
        )


class ShopPage(ListView):
    """
    A view for displaying products in a shop page.

    This class extends Django's ListView and is responsible for rendering the shop page
    template and fetching the appropriate products based on the provided category.

    Attributes:
        model (Model): The model used for fetching the products.
        template_name (str): The path to the template used for rendering the shop page.
        context_object_name (str): The variable name used for accessing the list of products in the template.
        paginate_by (int): The number of products to display per page.

    Methods:
        get_queryset(): Returns the queryset of products based on the provided category.
        get_context_data(**kwargs): Adds additional context data for rendering the template.

    """

    model = Product
    template_name = "website/shop.html"
    context_object_name = "products"
    paginate_by = 18

    def get_queryset(self):
        """
        Return the queryset of products based on the provided category.

        If the category is "all", all products are returned. Otherwise, products filtered by the category are returned.

        Returns:
            QuerySet: The queryset of products.
        """

        price = self.request.GET.get("price") or 0
        sizes = self.request.GET.getlist("sizes") or []
        colors = self.request.GET.getlist("colors") or []

        filter_kwargs = {}

        if sizes:
            filter_kwargs["sizes__name__in"] = sizes

        if colors:
            filter_kwargs["colors__name__in"] = colors

        category = self.kwargs["category"]
        if category == "all":
            return Product.objects.filter(price__gte=price, **filter_kwargs)

        return Product.objects.filter(
            category=category, price__gte=price, **filter_kwargs
        )

    def get_context_data(self, **kwargs):
        """
        Add additional context data for rendering the template.

        The context data includes the list of products, wishlist products (if user is authenticated as a customer),
        and the category.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)

        products = self.paginate_queryset(self.get_queryset(), self.paginate_by)[2]
        wishlist_products = []

        if self.request.user.is_authenticated and self.request.user.role == "customer":
            wishlist_products = filter(
                lambda product: product.wishlist_items.filter(
                    wishlist__user=self.request.user
                ),
                products,
            )

        min_price = Product.objects.aggregate(min_price=Min("price"))["min_price"]
        max_price = Product.objects.aggregate(max_price=Max("price"))["max_price"]

        context["wishlist_products"] = list(wishlist_products)
        context["category"] = self.kwargs["category"]
        context["min_price"] = min_price
        context["max_price"] = max_price
        context["all_colors"] = list(Color.objects.all().values_list("name", flat=True))
        context["all_sizes"] = list(Size.objects.all().values_list("name", flat=True))
        context["current_price"] = self.request.GET.get("price") or 0
        context["filtered_colors"] = self.request.GET.getlist("colors")
        context["filtered_sizes"] = self.request.GET.getlist("sizes")

        return context

import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from payment.models import OrderItem
from vendor.models import Product
from .models import CartItem, Cart, Wishlist, WishlistItem
from .forms import CartItemForm


def home_page(request):
    """
    Render the home page.

    Retrieves a list of products, selects 10 random products, and checks
    if the user is authenticated as a customer. If authenticated, filters the
    random products to include only those in the user's wishlist. Finally, renders
    the 'website/index.html' template with the list of random products and wishlist products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
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
    """
    Render the contact page.

    Renders the 'website/contact.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    return render(request, "website/contact.html")


def my_orders(request):
    """
    Render the orders page.

    Retrieves a list of ordered items associated with the currently authenticated user's orders.
    Renders the 'website/orders.html' template with the list of ordered items.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    ordered_items = OrderItem.objects.filter(order__user=request.user)
    return render(request, "website/orders.html", {"ordered_items": ordered_items})


def product_details(request, id):
    """
    View function for displaying product details.

    Retrieves the details of a product based on the provided `id` parameter and renders
    the product details page with relevant information.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the product to retrieve details for.

    Returns:
        HttpResponse: The HTTP response containing the rendered product details page.

    Raises:
        Product.DoesNotExist: If the product with the specified ID does not exist.

    """
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


class WishlistOperations:
    """
    Render the wishlist page for the logged-in user.

    Retrieves the wishlist items for the current user and renders the 'wishlist.html' template
    with the wishlist items.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered response with the wishlist items.

    """

    def wishlist_page(request):
        """
        Render the wishlist page with the user's wishlist items.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered wishlist page.

        """
        wishlist_items = WishlistItem.objects.filter(wishlist__user=request.user)
        return render(
            request, "website/wishlist.html", {"wishlist_items": wishlist_items}
        )

    def wishlist_operations(request, operation, id):
        """
        Perform operations on the wishlist items.

        Args:
            request (HttpRequest): The HTTP request object.
            operation (str): The operation to be performed. Possible values are "add" or "remove".
            id (int): The ID of the product associated with the operation.

        Returns:
            HttpResponseRedirect: Redirects back to the referring URL.

        """
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


class CartOperations:
    """
    This class provides operations related to the shopping cart functionality.

    Methods:
        cart_page(request):
            Retrieve and display the cart items for the authenticated user.

        add_to_cart(request, id):
            Add a product to the shopping cart based on the provided form data.

        cart_item_qty(request, operation, id):
            Perform quantity operations (increase, decrease, delete) on a cart item.
    """

    def cart_page(request):
        """
        Render the cart page with the cart items for the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered response with the cart items in the "cart.html" template.
        """
        cart_items = CartItem.objects.filter(cart__user=request.user)

        return render(request, "website/cart.html", {"cart_items": cart_items})

    def add_to_cart(request, id):
        """
        Add a product to the cart for the authenticated user.

        Args:
            request: The HTTP request object.
            id (int): The ID of the product to add to the cart.

        Returns:
            Redirects to the cart page after adding the product to the cart, or
            renders the "product-details.html" template with errors if the form is invalid.
        """
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
        """
        Update the quantity or delete a cart item for the authenticated user.

        Args:
            request: The HTTP request object.
            operation (str): The operation to perform on the cart item. Can be "increase", "decrease", or "delete".
            id (int): The ID of the cart item to update or delete.

        Returns:
            Redirects to the cart page after updating the cart item or deleting it.
        """
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
        category = self.kwargs["category"]
        if category == "all":
            return Product.objects.all()

        return Product.objects.filter(category=category)

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
                lambda product: product.wishlist_item.filter(
                    wishlist__user=self.request.user
                ),
                products,
            )

        context["wishlist_products"] = list(wishlist_products)
        context["category"] = self.kwargs["category"]
        return context

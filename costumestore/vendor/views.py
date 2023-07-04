from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DeleteView
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from payment.models import OrderItem
from costumestore.services import CloudinaryServices, HandelErrors
from .models import Product, Vendor, Color, Size
from .forms import ProductDetails


def is_vendor_verified(user):
    """
    Check if the user's vendor account is verified.

    Args:
        user (User): The user object.

    Returns:
        bool: True if the vendor account is verified, False otherwise.
    """
    return user.vendors.is_verified and user.vendors.is_document_added


def dashboard(request):
    """
    View function for the vendor dashboard.

    This function retrieves the vendor associated with the current user and fetches
    the 10 most recently updated products belonging to that vendor. It renders the
    'vendor/dashboard.html' template with the fetched products as the context.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTTP response with the 'vendor/dashboard.html' template and the
        fetched products as the context.
    """
    vendor = Vendor.objects.get(user=request.user)
    products = (
        Product.objects.filter(vendor=vendor).order_by("updated_at").reverse()[:10]
    )

    return render(request, "vendor/dashboard.html", context={"products": products})


class CompletedOrders(ListView):
    """
    A class-based view for displaying a list of completed orders for a specific vendor.

    Attributes:
        model (Model): The model to use for retrieving the orders.
        template_name (str): The name of the template used for rendering the view.
        context_object_name (str): The name of the context variable containing the orders.
        paginate_by (int): The number of orders to display per page.

    Methods:
        get_queryset(): Get the queryset of completed orders.
    """

    model = OrderItem
    template_name = "vendor/completed_orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        """
        Get the queryset of completed orders for the vendor.

        Returns:
            QuerySet: The queryset of completed orders.
        """
        orders = OrderItem.objects.filter(
            product__vendor__user=self.request.user, status="completed"
        ).order_by("updated_at")
        return orders


class Orders(ListView):
    """
    View class for displaying vendor orders.

    This class extends Django's ListView and provides a paginated list of orders
    associated with the current vendor.

    The orders are filtered based on the current user and their product's vendor.
    The 'vendor/orders.html' template is used to render the orders.

    Attributes:
        model: The model class to fetch the orders from (OrderItem).
        template_name: The name of the template to render ('vendor/orders.html').
        context_object_name: The name of the context variable to use for the orders ('orders').
        paginate_by: The number of orders to display per page (10).

    Methods:
        get_queryset: Returns the queryset of orders, filtered based on the current user
                      and their product's vendor.

    """

    model = OrderItem
    template_name = "vendor/orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        """
        Get the queryset of orders.

        This method filters the orders based on the current user and their product's vendor.
        It excludes orders with the status 'completed' and sorts the remaining orders by the
        'created_at' field.

        Returns:
            The filtered and sorted queryset of orders.
        """
        orders = (
            OrderItem.objects.filter(product__vendor__user=self.request.user)
            .exclude(status="completed")
            .order_by("created_at")
        )
        return orders


def update_order_status(request):
    """
    Update the status of an order item.

    This function takes a POST request containing the `order_item_id` and `status` parameters.

    It updates the corresponding order item's status in the database and redirects the user
    to the "orders" page.

    Args:
        request (HttpRequest): The HTTP request object containing the POST data.

    Returns:
        HttpResponseRedirect: A redirect response to the "orders" page.
    """
    order_item_id = request.POST.get("order_item_id")
    status = request.POST.get("status")

    OrderItem.objects.filter(id=order_item_id).update(status=status)
    return redirect("orders")


class Store(ListView):
    """
    View class for displaying a vendor's store.

    This class extends the ListView class and is responsible for rendering the "store.html" template.
    It retrieves the list of products associated with the current user's vendor and paginates the results.

    Attributes:
        model (Product): The model class to use for retrieving products.
        template_name (str): The path to the template used for rendering the store page.
        context_object_name (str): The variable name used for storing the product list in the context.
        paginate_by (int): The number of products to display per page.

    Methods:
        get_queryset: Returns the queryset of products associated with the current user's vendor.
    """

    model = Product
    template_name = "vendor/store.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        """
        Return the queryset of products associated with the current user's vendor.

        Returns:
            QuerySet: The queryset of products.
        """
        return Product.objects.filter(vendor__user=self.request.user)


class DeleteProduct(DeleteView):
    """
    A class-based view for deleting a specific Product object.

    Attributes:
        model (Model): The model to use for retrieving the Product object.
        queryset (QuerySet): The queryset of Product objects to be considered for deletion.
        slug_url_kwarg (str): The name of the URL keyword argument that contains the Product object's identifier.
        slug_field (str): The field used to retrieve the Product object from the database.
        success_url (str): The URL to redirect to after successful deletion.
    """

    model = Product
    queryset = Product.objects.all()
    slug_url_kwarg = "id"
    slug_field = "id"
    success_url = reverse_lazy("dashboard")


class AddProduct(View):
    """
    A class-based view for adding a new product.

    Methods:
        get(request): Handle GET requests and render the product add form.
        post(request): Handle POST requests and process the submitted form data.
    """

    @method_decorator(
        user_passes_test(is_vendor_verified, login_url=reverse_lazy("vendor_profile"))
    )
    def get(self, request):
        """
        Handle GET requests and render the product add form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response containing the rendered product add form.
        """
        colors = Color.objects.all()
        sizes = Size.objects.all()

        return render(
            request, "vendor/add_product.html", {"sizes": sizes, "colors": colors}
        )

    @method_decorator(
        user_passes_test(is_vendor_verified, login_url=reverse_lazy("vendor_profile"))
    )
    def post(self, request):
        """
        Handle POST requests and process the submitted form data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The response after processing the form data.
        """
        images = request.FILES.getlist("images")
        form = ProductDetails(request.POST)

        colors = Color.objects.all()
        sizes = Size.objects.all()

        if not form.is_valid():
            errors = HandelErrors.form_errors(form.errors, "dict")
            return render(
                request,
                "vendor/add_product.html",
                {
                    "data": form.cleaned_data,
                    "errors": errors,
                    "colors": colors,
                    "sizes": sizes,
                },
            )

        data = form.cleaned_data

        try:
            vendor = Vendor.objects.get(user=request.user)

            # Store documents in cloudinary
            images_url = []
            if len(images) > 0:
                for image in images:
                    result_dict = CloudinaryServices.store_image(
                        image=image,
                        folder="vendors/" + vendor.shop_name + "/products",
                        tags=[data["category"], data["subcategory"]],
                    )
                    images_url.append(result_dict)

            product = Product.objects.create(
                vendor=vendor,
                name=data["name"],
                category=data["category"],
                subcategory=data["subcategory"],
                rating=data["rating"],
                price=data["price"],
                discount=data["discount"],
                stock=data["stock"],
                description=data["description"],
                images=images_url,
            )

            for color in data["colors"]:
                instance, created = Color.objects.get_or_create(name=color)
                product.colors.add(instance)

            for size in data["sizes"]:
                instance, created = Size.objects.get_or_create(name=size)
                product.sizes.add(instance)

            messages.success(request, "Product details added successfully")
        except Exception as e:
            messages.error(request, "Something went wrong! Please try again.")

        return redirect("dashboard")


class EditProduct(View):
    """
    A class-based view for editing an existing product.

    Methods:
        get(request, id): Handle GET requests and render the product edit form.
        post(request, id): Handle POST requests and update the product with the submitted form data.
    """

    def get(self, request, id):
        """
        Handle GET requests and render the product edit form.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the product to be edited.

        Returns:
            HttpResponse: The response with the rendered product edit form.
        """
        colors = Color.objects.all()
        sizes = Size.objects.all()
        product = Product.objects.get(id=id)
        prod_colors = product.colors.all().values_list("name", flat=True)
        prod_sizes = product.sizes.all().values_list("name", flat=True)

        return render(
            request,
            "vendor/edit_product.html",
            context={
                "product": product,
                "colors": colors,
                "sizes": sizes,
                "prod_sizes": list(prod_sizes),
                "prod_colors": list(prod_colors),
            },
        )

    def post(self, request, id):
        """
        Handle POST requests and update the product with the submitted form data.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the product to be updated.

        Returns:
            HttpResponseRedirect: The redirect response to the dashboard.
        """
        images = request.FILES.getlist("images")
        form = ProductDetails(request.POST)

        colors = Color.objects.all()
        sizes = Size.objects.all()

        if not form.is_valid():
            errors = HandelErrors.form_errors(form.errors, "dict")
            return render(
                request,
                "vendor/add_product.html",
                {
                    "data": form.cleaned_data,
                    "errors": errors,
                    "colors": colors,
                    "sizes": sizes,
                },
            )

        data = form.cleaned_data

        try:
            vendor = Vendor.objects.get(user=request.user)
            old_product = Product.objects.get(id=id)

            # Store documents in cloudinary
            images_url = old_product.images
            if len(images) > 0:
                for image in images:
                    result_dict = CloudinaryServices.store_image(
                        image=image,
                        folder="vendors/" + vendor.shop_name + "/products",
                        tags=[data["category"], data["subcategory"]],
                    )
                    images_url = []
                    images_url.append(result_dict)

                # delete old images from cloudinary
                for image in old_product.images:
                    if image["public_id"]:
                        CloudinaryServices.delete_image(image_id=image["public_id"])

            product, created = Product.objects.update_or_create(
                id=id,
                defaults={
                    "name": data["name"],
                    "category": data["category"],
                    "subcategory": data["subcategory"],
                    "rating": data["rating"],
                    "price": data["price"],
                    "discount": data["discount"],
                    "stock": data["stock"],
                    "description": data["description"],
                    "images": images_url,
                },
            )

            for color in data["colors"]:
                instance, created = Color.objects.get_or_create(name=color)
                product.colors.add(instance)

            for size in data["sizes"]:
                instance, created = Size.objects.get_or_create(name=size)
                product.sizes.add(instance)

            messages.success(request, "Product details updated successfully")
        except Exception as e:
            messages.error(request, "Something went wrong! Please try again.")

        return redirect("dashboard")

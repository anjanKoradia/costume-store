from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from payment.models import OrderItem
from costumestore.services import CloudinaryServices
from .models import Product, Vendor
from .forms import ProductDetails


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


def delete_product(request, id):
    """
    Delete a product.

    This function takes the ID of a product as a parameter and deletes it from the database.
    After deleting the product, the user is redirected to the "dashboard" page.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the product to delete.

    Returns:
        HttpResponseRedirect: A redirect response to the "dashboard" page.
    """
    Product.objects.get(id=id).delete()
    return redirect("dashboard")


class AddProduct(View):
    """
    View for adding a product.

    This class-based view handles both GET and POST requests for adding a product.
    GET request renders the 'vendor/add_product.html' template.
    POST request processes the form data and creates a new Product instance.

    Methods:
        - get(request): Renders the 'vendor/add_product.html' template.
        - post(request): Processes the form data, uploads images to cloud storage, and 
                         creates a new Product instance.

    Returns:
        - GET request: Rendered HTML template.
        - POST request: Redirect to the 'dashboard' view.
    """

    def get(self, request):
        """
        Handles the GET request for adding a new product.

        This method renders the 'vendor/add_product.html' template for the GET request.

        Parameters:
            - request (HttpRequest): The HTTP GET request object.

        Returns:
            - HttpResponse: The HTTP response object containing the rendered template.

        """
        return render(request, "vendor/add_product.html")

    def post(self, request):
        """
        Handles the POST request for adding a new product.

        This method processes the form data from the POST request to create a new Product object. 
        It validates the form data, uploads images to a cloud storage service, and saves the 
        product details.

        Parameters:
            - request (HttpRequest): The HTTP POST request object.

        Returns:
            - HttpResponse: The HTTP response object for redirecting to the 'dashboard' URL.

        """
        images = request.FILES.getlist("images")
        form = ProductDetails(request.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            return render(
                request,
                "vendor/add_product.html",
                {"data": form.cleaned_data, "errors": errors},
            )

        data = form.cleaned_data

        try:
            vendor = Vendor.objects.get(user=request.user)

            # Store documents in cloudinary
            images_url = []
            if len(images) > 0:
                for image in images:
                    result_dict = CloudinaryServices.store_image(
                        image=image, folder=vendor.shop_name + "/products", 
                        tags=[data["category"], data["subcategory"]],
                    )
                    images_url.append(result_dict)

            Product.objects.create(
                vendor=vendor,
                name=data["name"],
                colors=data["colors"],
                dimension=data["dimension"],
                category=data["category"],
                subcategory=data["subcategory"],
                rating=data["rating"],
                price=data["price"],
                discount=data["discount"],
                stock=data["stock"],
                description=data["description"],
                images=images_url,
            )

        except Exception as e:
            print(e)

        return redirect("dashboard")


class EditProduct(View):
    """
    A class-based view for editing a product.

    This view allows a vendor to edit the details of a specific product. It handles both GET and POST requests.

    Methods:
        - get(request, id): Renders the edit_product.html template with the product details for the given ID.
        - post(request, id): Updates the product details based on the submitted form data 
          and handles image uploads and deletions.
    """

    def get(self, request, id):
        """
        Handle GET requests.

        Retrieves the product with the given ID from the database and renders the edit_product.html 
        template with the product details.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the product to be edited.

        Returns:
            HttpResponse: The HTTP response containing the rendered template.
        """
        product = Product.objects.get(pk=id)
        return render(
            request,
            "vendor/edit_product.html",
            context={"product": product},
        )

    def post(self, request, id):
        """
        Handle POST requests.

        Updates the product details based on the submitted form data and 
        handles image uploads and deletions.

        If the form data is not valid, it renders the edit_product.html template with the form 
        data and any validation errors.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the product being edited.

        Returns:
            HttpResponse: The HTTP response for the redirect to the dashboard.
        """
        images = request.FILES.getlist("images")
        form = ProductDetails(request.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            form.cleaned_data["id"] = id
            return render(
                request,
                "vendor/edit_product.html",
                {"product": form.cleaned_data, "errors": errors},
            )

        data = form.cleaned_data

        try:
            vendor = Vendor.objects.get(user=request.user)
            old_product = Product.objects.get(id=id)
        
            # Store documents in cloudinary
            images_url = []
            if len(images) > 0:
                for image in images:
                    result_dict = CloudinaryServices.store_image(
                        image=image, folder=vendor.shop_name + "/products",
                        tags=[data["category"], data["subcategory"]],
                    )
                    images_url.append(result_dict)

            Product.objects.update_or_create(
                id=id,
                defaults={
                    "name": data["name"],
                    "colors": data["colors"],
                    "dimension": data["dimension"],
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

            # delete old images from cloudinary
            for image in old_product.images:
                if image["public_id"]:
                    CloudinaryServices.delete_image(image_id=image["public_id"])

        except Exception as e:
            print(e)

        return redirect("dashboard")

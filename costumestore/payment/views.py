from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from accounts.models import Address
from .forms import BillingDetailsForm
from .models import Order, OrderItem, BillingDetail

def is_cart_items_available(user):
    if user.cart.cart_item.all().count() == 0:
        return False
    
    return True

class Checkout:
    """
    This class handles the checkout process for placing orders.

    The checkout process involves rendering the checkout page, validating
    the billing details form, creating an order, saving order items, creating
    or retrieving the billing address, and creating billing details. After a
    successful order placement, the user's cart is cleared, and they are
    redirected to the home page.

    Methods:
        checkout_page(request): To render the checkout page
        place_order(request): To place an order
    """

    @user_passes_test(is_cart_items_available, login_url="cart_page")
    def checkout_page(request):
        """
        Renders the checkout page with the user's default address and cart items.

        Args:
            request: The HTTP request object.

        Returns:
            A rendered HTML template displaying the checkout page with the user's default address
            and cart items.
        """
        address = request.user.address.get(type="Default")
        cart_items = request.user.cart.cart_item.all()

        return render(
            request,
            "payment/checkout.html",
            {"address": address, "cart_items": cart_items},
        )

    @user_passes_test(is_cart_items_available, login_url="cart_page")
    def place_order(request):
        """
        Handles the order placement process by validating the billing details form, creating an order,
        saving order items, creating or retrieving the billing address, creating billing details, and
        clearing the user's cart.

        Args:
            request: The HTTP request object.

        Returns:
            - If the form is valid and the order placement is successful, redirects
              the user to the home page.
            - If the form is invalid, renders the checkout page with the validation
              errors, user's default address, and cart items.
            - If an exception occurs during the order placement process, redirects
              the user to the home page.

        """
        address = request.user.address.get(type="Default")
        cart_items = request.user.cart.cart_item.all()

        form = BillingDetailsForm(request.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]

            return render(
                request,
                "payment/checkout.html",
                {"errors": errors, "address": address, "cart_items": cart_items},
            )

        data = form.cleaned_data

        try:
            order = Order.objects.create(
                user=request.user,
                amount=request.user.cart.total_price,
                order_note=data["order_note"],
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    color=item.color,
                )

            address, created = Address.objects.get_or_create(
                address=data["address"],
                city=data["city"],
                state=data["state"],
                country=data["country"],
                pin_code=data["pin_code"],
                user=request.user,
                defaults={"type": "Billing"},
            )

            BillingDetail.objects.create(
                order=order,
                name=data["name"],
                address=address,
                phone=data["phone"],
                email=data["email"],
            )

            request.user.cart.delete()

            return redirect("home_page")

        except Exception as e:
            print(e)
            return redirect("home_page")

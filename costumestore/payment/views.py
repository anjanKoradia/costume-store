from .models import Order, OrderItem, BillingDetail
from .forms import BillingDetailsForm
from accounts.models import Address
from django.shortcuts import render, redirect


class Checkout:
    def checkout_page(request):
        address = request.user.address.get(type="Default")
        cart_items = request.user.cart.cart_item.all()

        return render(
            request,
            "payment/checkout.html",
            {"address": address, "cart_items": cart_items},
        )

    def place_order(request):
        address = request.user.address.get(type="Default")
        cart_items = request.user.cart.cart_item.all()

        form = BillingDetailsForm(request.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            print(errors)
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
                defaults={
                    "type": "Billing"
                },
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

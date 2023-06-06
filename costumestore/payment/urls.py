from django.urls import path
from . import views

urlpatterns = [
    # checkout related routes
    path("customer/checkout/", views.Checkout.checkout_page, name="checkout_page"),
    path("customer/place-order/", views.Checkout.place_order, name="place_order"),
]

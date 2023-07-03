from django.urls import path
from . import views

urlpatterns = [
    # checkout related routes
    path("customer/order/", views.Checkout.as_view(), name="customer_order"),
]

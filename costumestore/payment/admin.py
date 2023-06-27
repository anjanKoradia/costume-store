from django.contrib import admin
from .models import Order, OrderItem, BillingDetail


@admin.register(Order)
class Orders(admin.ModelAdmin):
    """
    Admin configuration for the 'Orders' model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["user", "amount"]


@admin.register(OrderItem)
class OrderItems(admin.ModelAdmin):
    """
    Admin configuration for the 'OrderItems' model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["order", "product", "quantity", "status"]


@admin.register(BillingDetail)
class BillingDetails(admin.ModelAdmin):
    """
    Admin configuration for the 'BillingDetails' model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["order", "address", "name", "phone", "email"]

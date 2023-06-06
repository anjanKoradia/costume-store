from django.contrib import admin
from .models import Order, OrderItem, BillingDetail


@admin.register(Order)
class Cart(admin.ModelAdmin):
    list_display = ["user", "amount"]


@admin.register(OrderItem)
class Cart(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "status"]


@admin.register(BillingDetail)
class Cart(admin.ModelAdmin):
    list_display = ["order", "address", "name", "phone", "email"]

from django.contrib import admin
from .models import CartItem, Cart


@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display = [
        "user",
    ]


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = [
        "cart",
    ]

from django.contrib import admin
from .models import CartItem, Cart, Wishlist, WishlistItem


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


@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = [
        "user",
    ]


@admin.register(WishlistItem)
class WishlistItem(admin.ModelAdmin):
    list_display = [
        "wishlist",
    ]

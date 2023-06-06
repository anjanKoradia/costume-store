from django.contrib import admin
from .models import CartItem, Cart, Wishlist, WishlistItem


@admin.register(Cart)
class Cart(admin.ModelAdmin):
    list_display = ["user", "total_price"]


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ["cart", "product", "quantity", "size", "color"]


@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = ["user", "total_price"]


@admin.register(WishlistItem)
class WishlistItem(admin.ModelAdmin):
    list_display = ["wishlist", "product"]

from django.contrib import admin
from .models import Vendor, Address


@admin.register(Vendor)
class Vendors(admin.ModelAdmin):
    """
    Admin model for managing vendors.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["id", "shop_name"]


@admin.register(Address)
class Addresses(admin.ModelAdmin):
    """
    Admin model for managing addresses.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["id", "user"]

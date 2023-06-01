from django.contrib import admin
from .models import Vendor, Address


@admin.register(Vendor)
class Vendor(admin.ModelAdmin):
    list_display = ["id","shop_name"]

@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ["id","user"]
from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class Vendor(admin.ModelAdmin):
    list_display = ["id"]
from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class Products(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]

# @admin.register(ProductImage)
# class ProductImage(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "image",
#     ]
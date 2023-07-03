from django.contrib import admin
from .models import Product, Color, Size


@admin.register(Color)
class Colors(admin.ModelAdmin):
    """
    Admin configuration for the 'Color' model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["name"]


@admin.register(Size)
class Sizes(admin.ModelAdmin):
    """
    Admin configuration for the 'Size' model.

    Attributes:
        list_display (list): The fields to display in the admin list view.
    """

    list_display = ["name"]


# Register your models here.
@admin.register(Product)
class Products(admin.ModelAdmin):
    """
    Admin configuration for the Product model.

    This class defines the display options for the Product model in the Django admin interface.

    Attributes:
        list_display (list): A list of fields to display for each Product instance in the admin list view.
    """

    list_display = ["id", "name"]

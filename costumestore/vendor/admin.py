from django.contrib import admin
from .models import Product


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

from django.contrib import admin
from .models import User


@admin.register(User)
class BaseUser(admin.ModelAdmin):
    """
    Admin configuration for the User model.

    This class defines the display options for the User model in the Django admin interface.
    It extends the base admin.ModelAdmin class to customize the list view.

    Attributes:
        list_display (list): The fields to display in the list view of the User model.

    """

    list_display = ["id", "email", "name", "phone", "role"]

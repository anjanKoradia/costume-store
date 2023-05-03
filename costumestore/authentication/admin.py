from django.contrib import admin
from .models import User


@admin.register(User)
class BaseUser(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "name",
        "phone",
        "role"
    ]
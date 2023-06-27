import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager


class User(AbstractUser):
    """
    Custom user model representing a registered user in the system.

    This model extends Django's AbstractUser class and adds additional fields and functionality.

    Fields:
    - id (UUIDField): The unique identifier for the user (automatically generated).
    - email (EmailField): The user's email address (must be unique).
    - name (CharField): The user's name.
    - phone (CharField): The user's phone number.
    - role (CharField): The user's role (default is "customer").
    - profile_image (URLField): URL to the user's profile image (optional).
    - email_token (TextField): Token for email verification (optional).
    - is_active (BooleanField): Indicates whether the user is active or not (default is False).

    Additional Settings:
    - username, first_name, last_name: These fields are set to None to disable 
    them since email is used as the username.
    - objects: Custom user manager for this model.
    - USERNAME_FIELD: The field to be used as the unique identifier for authentication (set to "email").
    - REQUIRED_FIELDS: Additional required fields during user creation (empty list).

    Meta:
    - db_table: The database table name for this model.
    - verbose_name: The singular name for this model in the admin interface.
    - verbose_name_plural: The plural name for this model in the admin interface.
    """

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=9, default="customer")
    profile_image = models.URLField(blank=True, null=True)
    email_token = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import Vendor


class Product(models.Model):
    """
    A model representing a product.

    Each product has a unique identifier, belongs to a vendor, and contains various details such as name, colors,
    dimensions, category, subcategory, rating, price, discount, stock, images, description, and timestamps for creation
    and update.

    Attributes:
        id (UUIDField): The unique identifier for the product.
        vendor (ForeignKey): The vendor associated with the product.
        name (CharField): The name of the product.
        colors (CharField): The available colors for the product (optional).
        dimension (CharField): The dimensions of the product (optional).
        category (CharField): The category of the product.
        subcategory (CharField): The subcategory of the product (optional, default: "Clothing").
        rating (PositiveIntegerField): The rating of the product (0 to 5).
        price (PositiveIntegerField): The price of the product.
        discount (PositiveIntegerField): The discount percentage applied to the product (0 to 100, default: 0).
        stock (PositiveIntegerField): The available stock quantity of the product (default: 1).
        images (ArrayField): An array of JSON fields representing the images associated with the product.
        description (TextField): The description of the product.
        created_at (DateTimeField): The timestamp indicating when the product was created.
        updated_at (DateTimeField): The timestamp indicating when the product was last updated.

    Meta:
        db_table (str): The name of the database table for the model.
        verbose_name (str): The singular name for the model in the Django admin interface.
        verbose_name_plural (str): The plural name for the model in the Django admin interface.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="Product")
    name = models.CharField(max_length=200)
    colors = models.CharField(max_length=100, blank=True, default="")
    dimension = models.CharField(max_length=100, blank=True, default="")
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True, default="Clothing")
    rating = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    stock = models.PositiveIntegerField(default=1)
    images = ArrayField(models.JSONField())
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

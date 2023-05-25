from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from accounts.models import Vendor
from django.db import models
import uuid


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="Product")
    name = models.CharField(max_length=200)
    colors = models.CharField(max_length=100, blank=True, default="")
    dimension = models.CharField(max_length=100, blank=True, default="")
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True, default="Clothing")
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock = models.PositiveIntegerField(default=1)
    images = ArrayField(models.JSONField())
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

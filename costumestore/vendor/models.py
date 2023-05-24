from django.contrib.postgres.fields import ArrayField
from accounts.models import Vendor
from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="Product")
    name = models.CharField(max_length=200)
    colors = models.CharField(max_length=100, null=True, blank=True)
    dimension = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)
    images = ArrayField(models.JSONField())
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

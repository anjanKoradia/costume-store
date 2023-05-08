from django.db import models
import uuid


# Create your models here.
class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100,null=True, blank=True)
    dimensions = models.CharField(max_length=100,null=True, blank=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

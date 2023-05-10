from django.db import models
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("images/", filename)


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    image = models.ImageField(upload_to=get_file_path)

    class Meta:
        db_table = "product_images"
        verbose_name = "ProductImage"
        verbose_name_plural = "Product-Images"


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    colors = models.CharField(max_length=100, null=True, blank=True)
    dimension = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)
    description = models.TextField()
    images = models.ManyToManyField(ProductImage)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

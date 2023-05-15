from django.db.models.signals import post_delete
from django.dispatch import receiver
from accounts.models import Vendor
from django.conf import settings
from django.db import models
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("images/", filename)


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="Product")
    name = models.CharField(max_length=100)
    colors = models.CharField(max_length=100, null=True, blank=True)
    dimension = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ProductImages"
    )
    image = models.ImageField(upload_to=get_file_path)

    class Meta:
        db_table = "product_images"
        verbose_name = "ProductImage"
        verbose_name_plural = "Product-Images"


# delete product images from folder
@receiver(post_delete, sender=ProductImage)
def delete_saved_images(sender, instance, *args, **kwargs):
    try:
        path = os.path.join(settings.MEDIA_ROOT, "images")

        images = os.listdir(path)
        for image in images:
            if image.find(str(instance.image).split("/")[1]):
                os.remove(os.path.join(path, image))

    except Exception as e:
        print(e)

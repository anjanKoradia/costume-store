from django.db import models
import uuid


# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
#     id = models.UUIDField(default=uuid.uuid4(),primary_key=True)
#     address = models.TextField()
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     pincode = models.CharField(max_length=50)
#     country = models.CharField(max_length=50)
#     default = models.BooleanField(default=False)
    
#     class Meta:
#         db_table = "addresses"
#         verbose_name = "Address"
#         verbose_name_plural = "Addresses"


# class Cart(models.Model):
#     id = models.UUIDField(default=uuid.uuid4(),primary_key=True)
#     customer = models.OneToOneField("authentication.User", on_delete=models.CASCADE, related_name="carts")
#     # products = models.ManyToManyField(Product, on_delete=models.CASCADE, related_name="carts")
#     quantity = models.IntegerField(default=1)
    
#     class Meta:
#         db_table = "carts"
#         verbose_name = "Cart"
#         verbose_name_plural = "Carts"


class Vendor(models.Model):
    id = models.UUIDField(default=uuid.uuid4(),primary_key=True, editable=False)
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name="vendors")
    shop_name = models.CharField(max_length=100, null=True, blank=True)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    aadhar_image = models.ImageField(null=True, blank=True)
    pancard_number = models.CharField(max_length=10,null=True, blank=True)
    pancard_image = models.ImageField(null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    business_license = models.ImageField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_document_added = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "vendors"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

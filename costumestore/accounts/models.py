from django.db import models
import uuid


class Address(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4(), primary_key=True, unique=True, editable=False
    )
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="addresses"
    )
    address = models.TextField(blank=True)
    pin_code = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "addresses"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Vendor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        "authentication.User", on_delete=models.CASCADE, related_name="vendors"
    )
    shop_name = models.CharField(max_length=100, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
    aadhar_image = models.JSONField(null=True, blank=True)
    pancard_number = models.CharField(max_length=10, blank=True)
    pancard_image = models.JSONField(null=True, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    business_license = models.JSONField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_document_added = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendors"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

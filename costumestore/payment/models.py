from website.models import COLOR_CHOICES, SIZE_CHOICES
from django.core.validators import MinValueValidator
from accounts.models import Address
from vendor.models import Product
from django.db import models
import uuid

class Order(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name='order')
    amount = models.PositiveIntegerField()
    order_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_item"
    )
    status = models.CharField(max_length=10, default="placed")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    color = models.CharField(choices=COLOR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "order_items"
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
        

class BillingDetail(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="billing_detail")
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="billing_detail"
    )
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_details"
        verbose_name = "BillingDetail"
        verbose_name_plural = "BillingDetails"

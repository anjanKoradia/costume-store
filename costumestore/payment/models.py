import uuid
from django.core.validators import MinValueValidator
from django.db import models
from accounts.models import Address
from vendor.models import Product
from website.models import COLOR_CHOICES, SIZE_CHOICES


class Order(models.Model):
    """
    Model representing an order made by a user.

    Each order has a unique identifier, user reference, amount, order note, creation and update timestamps.

    Attributes:
        id (UUIDField): The unique identifier for the order.
        user (ForeignKey): Reference to the User model representing the user who made the order.
        amount (PositiveIntegerField): The amount associated with the order.
        order_note (TextField): A note or additional information about the order (optional).
        created_at (DateTimeField): The timestamp when the order was created.
        updated_at (DateTimeField): The timestamp when the order was last updated.

    Meta:
        db_table (str): The name of the database table for the Order model.
        verbose_name (str): The human-readable name for a single order instance.
        verbose_name_plural (str): The human-readable name for multiple order instances.
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="order"
    )
    amount = models.PositiveIntegerField()
    order_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    """
    Model representing an item within an order.

    Each order item has a unique identifier, reference to the parent order, associated product, status,
    quantity, size, color, and creation/update timestamps.

    Attributes:
        id (UUIDField): The unique identifier for the order item.
        order (ForeignKey): Reference to the Order model representing the parent order.
        product (ForeignKey): Reference to the Product model representing the associated product.
        status (CharField): The status of the order item.
        quantity (PositiveIntegerField): The quantity of the product in the order item.
        size (CharField): The size of the product in the order item.
        color (CharField): The color of the product in the order item.
        created_at (DateTimeField): The timestamp when the order item was created.
        updated_at (DateTimeField): The timestamp when the order item was last updated.

    Meta:
        db_table (str): The name of the database table for the OrderItem model.
        verbose_name (str): The human-readable name for a single order item instance.
        verbose_name_plural (str): The human-readable name for multiple order item instances.
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_item"
    )
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
    """
    Model representing the billing details associated with an order.

    Each billing detail has a unique identifier, reference to the parent order, name, address, phone number,
    email, and creation/update timestamps.

    Attributes:
        id (UUIDField): The unique identifier for the billing detail.
        order (OneToOneField): Reference to the Order model representing the parent order.
        name (CharField): The name associated with the billing detail.
        address (ForeignKey): Reference to the Address model representing the associated address.
        phone (CharField): The phone number associated with the billing detail.
        email (EmailField): The email associated with the billing detail.
        created_at (DateTimeField): The timestamp when the billing detail was created.
        updated_at (DateTimeField): The timestamp when the billing detail was last updated.

    Meta:
        db_table (str): The name of the database table for the BillingDetail model.
        verbose_name (str): The human-readable name for a single billing detail instance.
        verbose_name_plural (str): The human-readable name for multiple billing detail instances.
    """

    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="billing_detail"
    )
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

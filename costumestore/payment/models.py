from django.core.validators import MinValueValidator
from django.db import models
from accounts.models import Address
from vendor.models import Product
from common.models import BaseModel, SIZE_CHOICES


class Order(BaseModel):
    """
    Model representing an order made by a user.

    Each order has a unique identifier, user reference, amount, order note, creation and update timestamps.

    Attributes:
        user (ForeignKey): Reference to the User model representing the user who made the order.
        amount (PositiveIntegerField): The amount associated with the order.
        order_note (TextField): A note or additional information about the order (optional).

    Meta:
        db_table (str): The name of the database table for the Order model.
        verbose_name (str): The human-readable name for a single order instance.
        verbose_name_plural (str): The human-readable name for multiple order instances.
    """

    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="order"
    )
    amount = models.PositiveIntegerField()
    order_note = models.TextField(blank=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(BaseModel):
    """
    Model representing an item within an order.

    Each order item has a unique identifier, reference to the parent order, associated product, status,
    quantity, size, color, and creation/update timestamps.

    Attributes:
        order (ForeignKey): Reference to the Order model representing the parent order.
        product (ForeignKey): Reference to the Product model representing the associated product.
        status (CharField): The status of the order item.
        quantity (PositiveIntegerField): The quantity of the product in the order item.
        size (CharField): The size of the product in the order item.
        color (CharField): The color of the product in the order item.

    Meta:
        db_table (str): The name of the database table for the OrderItem model.
        verbose_name (str): The human-readable name for a single order item instance.
        verbose_name_plural (str): The human-readable name for multiple order item instances.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_item"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_item"
    )
    status = models.CharField(max_length=10, default="placed")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    color = models.CharField()

    class Meta:
        db_table = "order_items"
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"


class BillingDetail(BaseModel):
    """
    Model representing the billing details associated with an order.

    Each billing detail has a unique identifier, reference to the parent order, name, address, phone number,
    email, and creation/update timestamps.

    Attributes:
        order (OneToOneField): Reference to the Order model representing the parent order.
        name (CharField): The name associated with the billing detail.
        address (ForeignKey): Reference to the Address model representing the associated address.
        phone (CharField): The phone number associated with the billing detail.
        email (EmailField): The email associated with the billing detail.

    Meta:
        db_table (str): The name of the database table for the BillingDetail model.
        verbose_name (str): The human-readable name for a single billing detail instance.
        verbose_name_plural (str): The human-readable name for multiple billing detail instances.
    """

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="billing_detail"
    )
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="billing_detail"
    )
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    class Meta:
        db_table = "billing_details"
        verbose_name = "BillingDetail"
        verbose_name_plural = "BillingDetails"

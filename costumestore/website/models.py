from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor.models import Product
from django.db import models
import uuid

COLOR_CHOICES = (
    ("Red", "Red"),
    ("Blue", "Blue"),
    ("Green", "Green"),
    ("Yellow", "Yellow"),
    ("Black", "Black"),
    ("White", "White"),
    ("Gray", "Gray"),
    ("Pink", "Pink"),
    ("Purple", "Purple"),
    ("Orange", "Orange"),
    ("Brown", "Brown"),
    ("Silver", "Silver"),
    ("Gold", "Gold"),
    ("Navy", "Navy"),
    ("Teal", "Teal"),
    ("Maroon", "Maroon"),
    ("Olive", "Olive"),
    ("Coral", "Coral"),
    ("Turquoise", "Turquoise"),
    ("Beige", "Beige"),
)

SIZE_CHOICES = (
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("XXL", "Extra Extra Large"),
)


class Cart(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_item"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    color = models.CharField(choices=COLOR_CHOICES)

    class Meta:
        db_table = "cart_item"
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"


class Wishlist(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "wishlist"
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class WishlistItem(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlist_item"
    )

    class Meta:
        db_table = "wishlist_item"
        verbose_name = "WishlistItem"
        verbose_name_plural = "WishlistItems"


@receiver(post_save, sender=CartItem)
def my_post_save_receiver(sender, instance, created, **kwargs):
    if not created:
        if instance.quantity == 0:
            CartItem.objects.get(id=instance.id).delete()

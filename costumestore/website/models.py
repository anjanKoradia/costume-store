from django.db import models
from django.core.validators import MinValueValidator
from vendor.models import Product
from common.models import BaseModel, SIZE_CHOICES


class Cart(BaseModel):
    """
    Model representing a shopping cart.

    A shopping cart is associated with a user and contains cart items that represent
    the products added to the cart.

    Attributes:
        user (OneToOneField): The user associated with the cart.
        total_price (PositiveIntegerField): The total price of all items in the cart.

    Meta:
        db_table (str): The name of the database table for the Cart model.
        verbose_name (str): The human-readable name for a single cart object.
        verbose_name_plural (str): The human-readable name for multiple cart objects.
    """

    user = models.OneToOneField(
        "authentication.User", on_delete=models.CASCADE, related_name="cart"
    )
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(BaseModel):
    """
    Model representing an item in a shopping cart.

    An item in a shopping cart is associated with a cart and a product.

    Attributes:
        cart (ForeignKey): The cart to which the item belongs.
        product (ForeignKey): The product associated with the item.
        quantity (PositiveIntegerField): The quantity of the product in the cart.
        size (CharField): The size of the product.
        color (CharField): The color of the product.

    Meta:
        db_table (str): The name of the database table for the CartItem model.
        verbose_name (str): The human-readable name for a single cart item object.
        verbose_name_plural (str): The human-readable name for multiple cart item objects.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)
    color = models.CharField()

    class Meta:
        db_table = "cart_items"
        verbose_name = "CartItem"
        verbose_name_plural = "CartItems"


class Wishlist(BaseModel):
    """
    Model representing a user's wishlist.

    A wishlist is associated with a user and contains wishlist items that represent
    the products added to the wishlist.

    Attributes:
        user (OneToOneField): The user associated with the wishlist.
        total_price (PositiveIntegerField): The total price of all items in the wishlist.

    Meta:
        db_table (str): The name of the database table for the Wishlist model.
        verbose_name (str): The human-readable name for a single wishlist object.
        verbose_name_plural (str): The human-readable name for multiple wishlist objects.
    """

    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "wishlists"
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"


class WishlistItem(BaseModel):
    """
    Model representing an item in a wishlist.

    An item in a wishlist is associated with a wishlist and a product.

    Attributes:
        wishlist (ForeignKey): The wishlist to which the item belongs.
        product (ForeignKey): The product associated with the item.

    Meta:
        db_table (str): The name of the database table for the WishlistItem model.
        verbose_name (str): The human-readable name for a single wishlist item object.
        verbose_name_plural (str): The human-readable name for multiple wishlist item objects.
    """

    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="wishlist_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="wishlist_items"
    )

    class Meta:
        db_table = "wishlist_items"
        verbose_name = "WishlistItem"
        verbose_name_plural = "WishlistItems"

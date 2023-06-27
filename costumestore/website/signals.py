from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem, WishlistItem


@receiver(post_save, sender=CartItem)
def delete_cart_item(sender, instance, created, **kwargs):
    """
    Signal receiver for deleting a CartItem.

    This receiver is triggered after a CartItem is saved. If the instance's
    quantity is 0, the CartItem is deleted.

    Args:
        sender (Type): The sender class of the signal.
        instance (CartItem): The instance of the CartItem being saved.
        created (bool): Indicates whether the CartItem was created or updated.
        kwargs: Additional keyword arguments.
    """
    if not created:
        if instance.quantity == 0:
            CartItem.objects.get(id=instance.id).delete()


@receiver(post_delete, sender=CartItem)
def update_cart(sender, instance, **kwargs):
    """
    Signal receiver for updating the associated Cart when a CartItem is deleted.

    This receiver is triggered after a CartItem is deleted. It updates the
    total_price of the associated Cart by subtracting the price of the deleted CartItem.

    Args:
        sender (Type): The sender class of the signal.
        instance (CartItem): The instance of the CartItem being deleted.
        kwargs: Additional keyword arguments.
    """
    cart = instance.cart
    cart.total_price = cart.total_price - (instance.product.price * instance.quantity)
    cart.save()


@receiver(post_delete, sender=WishlistItem)
def update_wishlist(sender, instance, **kwargs):
    """
    Signal receiver for updating the associated Wishlist when a WishlistItem is deleted.

    This receiver is triggered after a WishlistItem is deleted. It updates the
    total_price of the associated Wishlist by subtracting the price of the deleted WishlistItem.

    Args:
        sender (Type): The sender class of the signal.
        instance (WishlistItem): The instance of the WishlistItem being deleted.
        kwargs: Additional keyword arguments.
    """
    wishlist = instance.wishlist
    wishlist.total_price = wishlist.total_price - instance.product.price
    wishlist.save()

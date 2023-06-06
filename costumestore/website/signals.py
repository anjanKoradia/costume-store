from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem, WishlistItem


@receiver(post_save, sender=CartItem)
def delete_cart_item(sender, instance, created, **kwargs):
    if not created:
        if instance.quantity == 0:
            CartItem.objects.get(id=instance.id).delete()


@receiver(post_delete, sender=CartItem)
def update_cart(sender, instance, **kwargs):
    cart = instance.cart
    cart.total_price = cart.total_price - (instance.product.price * instance.quantity)
    cart.save()


@receiver(post_delete, sender=WishlistItem)
def update_wishlist(sender, instance, **kwargs):
    wishlist = instance.wishlist
    wishlist.total_price = wishlist.total_price - instance.product.price
    wishlist.save()
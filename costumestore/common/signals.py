import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from website.models import Cart, Wishlist, CartItem, WishlistItem
from accounts.models import Address, Vendor
from common.services import send_account_activation_email
from authentication.models import User


# signal to create vendor profile and to send account activation email
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a profile for a newly created User instance.

    This function is triggered by the post_save signal when a User instance is saved.
    It creates a profile for the user by performing the following actions:
    - Generates an email token using a UUID and assigns it to the user's email_token field.
    - Creates an Address instance associated with the user.
    - If the user's role is "vendor", creates a Vendor instance associated with the user.
    - If the user's role is "customer", creates a Cart and Wishlist instance associated with the user.

    Args:
        sender: The model class that sends the signal (User in this case).
        instance: The actual instance being saved (the newly created User instance).
        created: A boolean indicating if the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If any error occurs during the profile creation process.

    """
    try:
        if created:
            email_token = str(uuid.uuid4())
            user = User.objects.get(email=instance.email)
            user.email_token = email_token
            user.save()

            Address.objects.create(user=instance)
            send_account_activation_email(instance.name, instance.email, email_token)
            if instance.role == "vendor":
                Vendor.objects.create(user=instance)

            if instance.role == "customer":
                Cart.objects.create(user=instance)
                Wishlist.objects.create(user=instance)

    except Exception as e:
        print(e)


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

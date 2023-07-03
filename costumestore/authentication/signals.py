import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from website.models import Cart, Wishlist
from accounts.models import Address, Vendor
from .models import User
from .services import send_account_activation_email


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
            send_account_activation_email(instance.name,instance.email,email_token)
            if instance.role == "vendor":
                Vendor.objects.create(user=instance)

            if instance.role == "customer":
                Cart.objects.create(user=instance)
                Wishlist.objects.create(user=instance)

    except Exception as e:
        print(e)

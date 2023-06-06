from .services import send_account_activation_email
from django.db.models.signals import post_save
from accounts.models import Address, Vendor
from website.models import Cart, Wishlist
from django.dispatch import receiver
from .models import User
import uuid


# signal to create vendor profile and to send account activation email
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            user = User.objects.get(email=instance.email)
            user.email_token = email_token
            user.save()

            Address.objects.create(user=instance)

            # send_account_activation_email(instance.name,instance.email,email_token)
            if instance.role == "vendor":
                Vendor.objects.create(user=instance)

            if instance.role == "customer":
                Cart.objects.create(user=instance)
                Wishlist.objects.create(user=instance)

    except Exception as e:
        print(e)

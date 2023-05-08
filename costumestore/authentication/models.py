from .services import send_account_activation_email
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from .manager import CustomUserManager
from django.dispatch import receiver
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=9, default="customer")
    profile_image = models.URLField(blank=True, null=True)
    email_token = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            user = User.objects.get(email=instance.email)
            user.email_token = email_token
            user.save()
            
            send_account_activation_email(instance.name,instance.email,email_token)
            
    except Exception as e:
        print(e)
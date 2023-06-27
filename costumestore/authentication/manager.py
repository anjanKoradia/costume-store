from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for the User model.

    This class provides methods to create regular users and superusers.

    Attributes:
        use_in_migrations (bool): Indicates whether the manager should be used in migrations.

    Methods:
        create_user(email, password=None, **extra_fields): Creates a new user.
        create_superuser(email, password=None, **extra_fields): Creates a new superuser.
    """

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a new user.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user.
            **extra_fields: Additional fields to be set for the user.

        Returns:
            User: The newly created user.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a new superuser.

        Args:
            email (str): The email address of the superuser.
            password (str, optional): The password for the superuser.
            **extra_fields: Additional fields to be set for the superuser.

        Returns:
            User: The newly created superuser.

        Raises:
            ValueError: If is_staff or is_superuser fields are not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

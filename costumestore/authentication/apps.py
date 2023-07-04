from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    AppConfig for the authentication app.

    This class provides the configuration for the authentication app in Django.

    Attributes:
        default_auto_field (str): The default auto field for the authentication models.
        name (str): The name of the authentication app.

    Methods:
        ready(): Performs any initialization tasks when the app is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"

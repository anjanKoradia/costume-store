from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for the 'accounts' app.

    Attributes:
        default_auto_field (str): The default auto field for model primary keys.
        name (str): The name of the app ('accounts').
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

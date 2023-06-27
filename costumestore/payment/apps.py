from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """
    Configuration for the 'payment' app.

    Attributes:
        default_auto_field (str): The default auto field for model primary keys.
        name (str): The name of the app ('payment').

    Methods:
        ready(): Performs actions when the app is ready to be used.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

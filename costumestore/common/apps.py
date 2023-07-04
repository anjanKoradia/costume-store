from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    AppConfig for the common app.

    This class provides the configuration for the common app in Django.

    Attributes:
        default_auto_field (str): The default auto field for the common models.
        name (str): The name of the common app.

    Methods:
        ready(): Performs any initialization tasks when the app is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "common"

    def ready(self) -> None:
        import common.signals

        return super().ready()

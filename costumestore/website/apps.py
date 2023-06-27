from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    """
    Configuration for the 'website' app.

    Attributes:
        default_auto_field (str): The default auto field for model primary keys.
        name (str): The name of the app ('website').
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'
    
    def ready(self) -> None:
        import website.signals
        return super().ready()

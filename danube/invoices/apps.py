from importlib import import_module

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "danube.invoices"

    def ready(self) -> None:
        """Ready app."""
        import_module("danube.invoices.signals")

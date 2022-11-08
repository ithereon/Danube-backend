from importlib import import_module

from django.apps import AppConfig


class QuotesConfig(AppConfig):
    name = "danube.quotes"

    def ready(self) -> None:
        """Ready app."""
        import_module("danube.quotes.signals")

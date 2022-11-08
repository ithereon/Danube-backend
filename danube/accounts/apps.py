from importlib import import_module

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "danube.accounts"

    def ready(self) -> None:
        """Ready app."""
        import_module("danube.accounts.signals")

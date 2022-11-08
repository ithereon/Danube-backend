from importlib import import_module

from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'danube.payments'

    # def ready(self) -> None:
    #     """Ready app."""
    #     import_module("danube.payments.signals")

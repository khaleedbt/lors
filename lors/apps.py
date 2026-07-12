from django.apps import AppConfig


class LorsConfig(AppConfig):
    name = 'lors'

    def ready(self):
        from . import schema  # noqa: F401 registers drf-spectacular field extensions

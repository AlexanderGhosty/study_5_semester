from django.apps import AppConfig


class NestedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nested_app'

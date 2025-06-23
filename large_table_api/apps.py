from django.apps import AppConfig


class LargeTableApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "large_table_api"

from django.apps import AppConfig


class MapToDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'map_to_db'
    verbose_name: str = 'Options'

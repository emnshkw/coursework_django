from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    verbose_name = 'Преподаватели'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth'

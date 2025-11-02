# App configuration for the core application
# Registers the app within Django and sets the default primary key type for models

from django.apps import AppConfig

class CoreConfig(AppConfig):
    # use BigAutoField for all primary keys by default
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

from django.apps import AppConfig


class TenantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tenants'
    verbose_name = 'Tenants'

    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.tenants.signals  # noqa
        except ImportError:
            pass
from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.subscription"

    def ready(self):
        from apps.shared.caching.helpers import generate_version_keys
        from apps.shared.caching.signals import register_versioned_cache_signals

        from .models import Plan

        LIST_VERSION_KEY, DETAIL_VERSION_KEY = generate_version_keys("Plan")

        register_versioned_cache_signals(
            sender=Plan,
            list_version_key=LIST_VERSION_KEY,
            detail_version_key=DETAIL_VERSION_KEY,
        )

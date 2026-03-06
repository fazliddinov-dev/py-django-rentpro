# apps/shared/caching/signals.py
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


def register_versioned_cache_signals(
    sender, list_version_key=None, detail_version_key=None
):
    """
    Automatically attach signals to a model to bump cache versions.

    - sender: Django model class
    - list_version_key: Redis key for list cache version
    - detail_version_key: Redis key for detail cache version
    """
    if list_version_key:

        @receiver([post_save, post_delete], sender=sender)
        def bump_list_version(sender, instance, **kwargs):
            try:
                cache.incr(list_version_key)
            except ValueError:
                cache.set(list_version_key, 2)

    if detail_version_key:

        @receiver([post_save, post_delete], sender=sender)
        def bump_detail_version(sender, instance, **kwargs):
            try:
                cache.incr(detail_version_key)
            except ValueError:
                cache.set(detail_version_key, 2)

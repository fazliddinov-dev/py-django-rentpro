from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import SubscriptionProducts

LIST_VERSION_KEY = "subscription_products:list_version"
DETAIL_VERSION_KEY = "subscription_products:detail_version"


def bump_version(key):
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 2)


@receiver([post_save, post_delete], sender=SubscriptionProducts)
def invalidate_subscription_product_cache(sender, instance, **kwargs):
    bump_version(LIST_VERSION_KEY)
    bump_version(DETAIL_VERSION_KEY)

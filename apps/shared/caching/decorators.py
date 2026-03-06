from functools import wraps
from urllib.parse import urlencode

from django.core.cache import cache
from rest_framework.response import Response

DEFAULT_TTL = 60 * 60 * 24  # 24 hours


def versioned_cache(
    list_version_key=None, detail_version_key=None, ttl=DEFAULT_TTL, user_scope=False
):
    """
    Decorator for DRF list, retrieve, or custom methods using versioned caching.

    - list_version_key: Redis key for list cache version
    - detail_version_key: Redis key for detail cache version
    - ttl: cache expiration in seconds
    - user_scope: if True, cache is separated per user (user.id)
    """

    def decorator(func):
        @wraps(func)
        def wrapped(self, request, *args, **kwargs):
            # Determine type of endpoint
            is_list = func.__name__ == "list"
            is_detail = func.__name__ == "retrieve" or "pk" in kwargs

            # Build cache key
            key_parts = []

            if is_list and list_version_key:
                version = cache.get(list_version_key) or 1
                key_parts.append(f"{list_version_key}:v{version}")
                # include query params
                if request.GET:
                    key_parts.append(urlencode(request.GET))
            elif is_detail and detail_version_key:
                version = cache.get(detail_version_key) or 1
                obj_id = kwargs.get("pk", "unknown")
                key_parts.append(f"{detail_version_key}:{obj_id}:v{version}")
            else:
                # Other methods: don't cache
                return func(self, request, *args, **kwargs)

            if user_scope and getattr(request.user, "id", None):
                key_parts.append(f"user:{request.user.id}")

            cache_key = ":".join(key_parts)

            # Return cached response if exists
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)

            # Call the original method
            response = func(self, request, *args, **kwargs)

            # Save to cache
            cache.set(cache_key, response.data, ttl)
            return response

        return wrapped

    return decorator

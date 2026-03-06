# apps/subscription/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from apps.shared.auth.authentication import SuperAdminJWTAuthentication
from apps.shared.auth.permissions import IsSuperAdmin
from apps.shared.caching.decorators import versioned_cache
from apps.shared.caching.helpers import generate_version_keys

from ..filters import SubscriptionProductFilter
from ..models import SubscriptionProducts
from ..serializers import SubscriptionProductSerializer

LIST_VERSION_KEY, DETAIL_VERSION_KEY = generate_version_keys("SubscriptionProducts")


class SubscriptionProductViewSet(ModelViewSet):
    queryset = SubscriptionProducts.objects.all()
    serializer_class = SubscriptionProductSerializer
    authentication_classes = [SuperAdminJWTAuthentication]
    permission_classes = [IsSuperAdmin]
    pagination_class = None
    filterset_class = SubscriptionProductFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]
    ordering_fields = [
        "regular_price",
        "sale_price",
        "sms_count",
        "stock_count",
        "length",
        "period",
    ]
    ordering = ["-regular_price"]

    @versioned_cache(list_version_key=LIST_VERSION_KEY, ttl=60 * 60 * 24)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @versioned_cache(detail_version_key=DETAIL_VERSION_KEY, ttl=60 * 60 * 24)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

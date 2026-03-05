from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.subscription.views.subscription_product_view import SubscriptionProductViewSet

router = DefaultRouter()
router.register(
    r"subscription-product", SubscriptionProductViewSet, basename="subscription-product"
)

urlpatterns = [
    path("", include(router.urls)),
]

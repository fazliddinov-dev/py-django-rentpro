from rest_framework.viewsets import ModelViewSet

from ..models import SubscriptionProducts
from ..serializers import SubscriptionProductSerializer


class SubscriptionProductViewSet(ModelViewSet):
    queryset = SubscriptionProducts.objects.all()
    serializer_class = SubscriptionProductSerializer

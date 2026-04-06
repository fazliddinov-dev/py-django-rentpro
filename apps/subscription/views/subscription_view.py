from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SubscriptionSerializer
from ..services import SubscriptionService


class SubscriptionView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription_id = SubscriptionService.create_subscription(
            user=request.user, data=serializer.validated_data
        )

        return Response(
            {"subscription_id": subscription_id}, status=status.HTTP_201_CREATED
        )

from rest_framework import serializers

from .models import SubscriptionProducts


class SubscriptionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionProducts
        fields = "__all__"

from django.db import IntegrityError
from rest_framework import serializers

from .models import SubscriptionProducts


class SubscriptionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionProducts
        fields = "__all__"
        extra_kwargs = {
            "order": {"read_only": True}  # ignored on create, returned in response
        }

    def update(self, instance, validated_data):
        # Allow order update if client provides it
        if "order" in self.initial_data:
            instance.order = self.initial_data["order"]

        try:
            instance.save()
        except IntegrityError as e:  # <-- use IntegrityError, not InterruptedError
            if "unique" in str(e).lower() and "order" in str(e).lower():
                raise serializers.ValidationError(
                    {"order": "This order value already exists."}
                )
            raise e

        return instance

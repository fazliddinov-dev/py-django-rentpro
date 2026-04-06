from django.db import IntegrityError
from rest_framework import serializers

from .models import Plan, Subscription


class Planserializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
        extra_kwargs = {
            "order": {"read_only": True}  # ignored on create, returned in response
        }

    def update(self, instance, validated_data):
        # If 'order' is provided in the request data, allow updating it
        request = self.context.get("request")
        if request and "order" in request.data:
            instance.order = request.data["order"]

        # Update all other validated fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source="company.id")

    class Meta:
        model = Subscription
        fields = ["company", "plan"]

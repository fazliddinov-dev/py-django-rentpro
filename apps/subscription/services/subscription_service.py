from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Subscription


class SubscriptionService:
    @staticmethod
    @transaction.atomic
    def create_subscription(user, data):
        if Subscription.objects.filter(
            company=user.company, status=Subscription.Status.ACTIVE
        ).exists():
            raise ValidationError("Active subscription already exists")

        start_date = timezone.now()
        end_date = data["plan"].calculate_end_date(start_date)

        subscription = Subscription.objects.create(
            company=user.company,  # 🔐 secure source
            plan=data["plan"],
            start_date=start_date,
            end_date=end_date,
            status=Subscription.Status.PENDING,
            payment_status=Subscription.PaymentStatus.PENDING,
        )

        return subscription.id

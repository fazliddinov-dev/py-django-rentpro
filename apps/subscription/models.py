from datetime import timedelta

from django.db import models, transaction

from ..user.models import Company


class Plan(models.Model):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"

    SUBSCRIPTION_PERIOD_CHOICES = [
        (DAY, "Kun"),
        (MONTH, "Oy"),
        (YEAR, "Yil"),
    ]

    name = models.CharField(max_length=255, unique=True)

    regular_price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    sms_count = models.PositiveIntegerField()
    stock_count = models.PositiveIntegerField()
    length = models.PositiveIntegerField()

    period = models.CharField(choices=SUBSCRIPTION_PERIOD_CHOICES, max_length=255)

    info = models.TextField()

    is_visible = models.BooleanField(default=True)

    order = models.PositiveIntegerField(unique=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.order:
            # atomic block ensures no race condition
            with transaction.atomic():
                # lock the table rows for update
                max_order = (
                    Plan.objects.select_for_update().aggregate(models.Max("order"))[
                        "order__max"
                    ]
                    or 0
                )
                self.order = max_order + 1
        super().save(*args, **kwargs)

    def calculate_end_date(self, start_date):
        if self.period == self.DAY:
            return start_date + timedelta(days=self.length)
        elif self.period == self.MONTH:
            return start_date + timedelta(days=30 * self.length)
        elif self.period == self.YEAR:
            return start_date + timedelta(days=365 * self.length)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"
        PENDING = "pending", "Pending"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company"],
                condition=models.Q(status="active"),
                name="one_active_subscription_per_company",
            )
        ]

    def __str__(self):
        return f"{self.company} - {self.plan}"

from django.core.validators import MinValueValidator
from django.db import models, transaction


class SubscriptionProducts(models.Model):
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
                    SubscriptionProducts.objects.select_for_update().aggregate(
                        models.Max("order")
                    )["order__max"]
                    or 0
                )
                self.order = max_order + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

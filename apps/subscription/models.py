from django.core.validators import MinValueValidator
from django.db import models


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

    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name

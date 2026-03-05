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

    product_name = models.CharField(max_length=255, unique=True)
    regular_price = models.IntegerField()
    sale_price = models.IntegerField()
    sms_count = models.IntegerField()
    stock_count = models.IntegerField()
    subscription_length = models.IntegerField()
    subscription_period = models.CharField(choices=SUBSCRIPTION_PERIOD_CHOICES)
    subscription_info = models.TextField()
    is_visible = models.BooleanField(default=True)
    order = models.IntegerField()

    def __str__(self):
        return self.product_name

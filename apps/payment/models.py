from django.db import models


# Create your models here.
class Payment(models.Model):
    # split payments into for subscription and for orders
    class PaymentCause(models.TextChoices):
        SUBSCRIPTION = "subscription", "Subscription"
        ORDER = "order", "Order"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    payment_cause = models.CharField(
        max_length=20, choices=PaymentCause.choices, default=PaymentCause.ORDER
    )

    def __str__(self):
        return f"Payment {self.id} for Order {self.order_id}"

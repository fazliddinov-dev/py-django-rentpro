from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        STAFF = "staff", "Staff"
        CUSTOMER = "customer", "Customer"

    username = None

    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)

    role = models.CharField(max_length=20, choices=Role.choices)

    # Tenant
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class Company(models.Model):
    name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default="UTC")
    address = models.TextField(blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_companies",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="customer_profile"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="customers"
    )

    is_blacklist = models.BooleanField(default=False)

    class Meta:
        unique_together = ("company", "user")


class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)

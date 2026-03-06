from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=50, unique=True)
    mfo = models.CharField(max_length=50)
    website = models.URLField(max_length=255, blank=True, null=True)
    bank_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="vendors"
    )

    def __str__(self):
        return self.full_name


class TeamMember(models.Model):
    class RoleChoices(models.TextChoices):
        MANAGER = "manager", "Manager"
        WAREHOUSE_MANAGER = "warehouse_manager", "Warehouse manager"
        ASSISTANT = "assistant", "Assistant"
        DRIVER = "driver", "Driver"

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="team_members"
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=RoleChoices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "email"], name="unique_team_email_per_vendor"
            ),
            models.UniqueConstraint(
                fields=["vendor", "phone_number"], name="unique_team_phone_per_vendor"
            ),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class Customer(models.Model):
    class TypeChoices(models.TextChoices):
        BAD = "bad", "Bad"
        GOOD = "good", "Good"
        PERFECT = "perfect", "Perfect"

    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="customers"
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=255)

    customer_type = models.CharField(
        max_length=20, choices=TypeChoices, default=TypeChoices.GOOD
    )
    is_blacklist = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "phone_number"],
                name="unique_customer_phone_per_vendor",
            )
        ]

    def __str__(self):
        return self.full_name

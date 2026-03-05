from django.db import models
from django.db.models import EmailField


class UserModel(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self) -> EmailField:
        return self.email

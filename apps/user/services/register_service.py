from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

@transaction.atomic
def register_user(data):
    user = User.objects.create(
        email=data['email'],
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        role=User.Role.OWNER,
    )

    user.set_password(data['password'])
    user.save()

    return user
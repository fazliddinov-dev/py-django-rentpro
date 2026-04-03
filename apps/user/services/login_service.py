# services/login_service.py
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import PermissionDenied, ValidationError

User = get_user_model()


class LoginService:
    @staticmethod
    def login(email: str, password: str):
        """
        Validates credentials and returns user.
        """
        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError("Invalid email or password.")

        if not user.is_active:
            raise PermissionDenied("Account is disabled.")

        return user

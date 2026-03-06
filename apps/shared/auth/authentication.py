import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .models import SuperAdminUser


class SuperAdminJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None

        try:
            payload = jwt.decode(
                token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        # Only super admin role
        role = payload.get("role")
        if role != "super_admin":
            raise exceptions.AuthenticationFailed("Unauthorized")

        # Return user-like object
        user = SuperAdminUser(role=role)
        return (user, token)

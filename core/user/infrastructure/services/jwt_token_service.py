import jwt
from django.conf import settings

from core.user.application.interfaces.token_service import TokenService


class JWTTokenService(TokenService):
    def generate_access_token(self, user_id: int) -> str:
        payload = {"user_id": user_id}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

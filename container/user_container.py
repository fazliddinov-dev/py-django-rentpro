from core.user.application.use_cases.login_user import LoginUserUseCase
from core.user.infrastructure.db.repositories.django_user_repository import (
    DjangoUserRepository,
)
from core.user.infrastructure.services.django_password_hasher import (
    DjangoPasswordHasher,
)
from core.user.infrastructure.services.jwt_token_service import JWTTokenService


def login_user_use_case():
    return LoginUserUseCase(
        user_repo=DjangoUserRepository(),
        token_service=JWTTokenService(),
        password_hasher=DjangoPasswordHasher,
    )

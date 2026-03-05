from core.user.application.interfaces.user_repository import UserRepository
from core.user.domain.entities.user import User
from core.user.infrastructure.db.models.user_model import UserModel


class DjangoUserRepository(UserRepository):
    def get_by_email(self, email: str):
        try:
            obj = UserModel.objects.get(email=email)
            return User(
                id=obj.id,  # type: ignore[attr-defined]
                email=obj.email,
                password_hash=obj.password,
            )
        except UserModel.DoesNotExist:
            return None

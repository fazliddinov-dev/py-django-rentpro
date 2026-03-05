from django.contrib.auth.hashers import check_password

from core.user.domain.services.password_hasher import PasswordHasher


class DjangoPasswordHasher(PasswordHasher):
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return check_password(raw_password, hashed_password)

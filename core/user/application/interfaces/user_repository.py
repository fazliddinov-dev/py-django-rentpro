from abc import ABC, abstractmethod

from core.user.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

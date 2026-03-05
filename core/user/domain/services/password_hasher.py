from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        pass

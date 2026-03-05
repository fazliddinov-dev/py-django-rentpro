from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    def generate_access_token(self, user_id: int) -> str:
        pass

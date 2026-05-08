from abc import ABC, abstractmethod

from app.models.refresh_token import RefreshToken

class ITokenRepository(ABC):
    @abstractmethod
    def create_refresh_token(self, new_token: RefreshToken) -> None:
        pass

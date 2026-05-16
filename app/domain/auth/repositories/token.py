from typing import Protocol
from app.models.refresh_token import RefreshToken

class TokenRepository(Protocol):
    def create_refresh_token(self, new_token: RefreshToken) -> None: ...

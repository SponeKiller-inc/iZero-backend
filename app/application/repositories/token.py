from typing import Protocol
from app.application.dto.token import RefreshToken

class TokenRepository(Protocol):
    def create_refresh_token(self, new_token: RefreshToken) -> None: ...

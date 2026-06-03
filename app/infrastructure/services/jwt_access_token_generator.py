from datetime import datetime

from jose import JWTError, jwt

from app.application.dto.auth.token import TokenPayload
from app.application.exceptions.auth import AccessTokenProviderError
from app.infrastructure.services.time_provider import SystemTimeProvider


class JwtAccessTokenGenerator:

    def __init__(self, secret_key: str, algorithm: str = "HS256"):

        self._secret_key = secret_key
        self._algorithm = algorithm

    def encode(self, user_id: int, expires_at: datetime) -> str:
        """
        Encodes JWT token

        Args:
            user_id (int): user_id
            expires_at (datetime): expiration time (UTC)

        Returns:
            str: JWT token
        """
        payload = {
            "sub": str(user_id),
            "exp": int(expires_at.timestamp())
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode(self, token: str) -> TokenPayload:
        """
        Decodes JWT token

        Args:
            token (str): JWT token

        Returns:
            TokenPayload: Token payload

        Raises:
            AccessTokenProviderError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token, 
                self._secret_key, 
                algorithms=[self._algorithm]
            )

            user_id = payload.get("sub")
            if not user_id or not str(user_id).isdigit():
                raise AccessTokenProviderError(
                    "Invalid token payload: user_id missing or non-numeric"
                )
            
            expired_at = payload.get("exp")
            if not expired_at:
                raise AccessTokenProviderError("Invalid token payload: expired_at missing")
            
            return TokenPayload(
                user_id=int(user_id),
                expired_at=SystemTimeProvider.from_timestamp(expired_at)
            )
            
        except JWTError as e:
            raise AccessTokenProviderError(f"Invalid or expired token: {e}") from e
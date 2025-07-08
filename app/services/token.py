import secrets
from datetime import datetime

from jose import JWTError, jwt

from app.repositories.token import TokenRepository
from app.models.refresh_token import RefreshToken
from app.utils.config import settings
from app.utils.utils import create_UTC_exp_time

from app.exceptions.infrastucture.repository import CreateExecutionError
from app.exceptions.domain.token import (
    RefreshTokenServiceError,
    AccessTokenServiceError,
    CSRFTokenCreationError,
)
from app.exceptions.repository.token import RefreshTokenCreationError

class TokenService:
    def __init__(
        self, 
        repo: TokenRepository,
    ):
        self.repo = repo
    
    def create_access_token(self, user_id: int) -> str:
        """
        Create access token

        Args:
            user_id (int): user id
            
        Returns:
            str: JWT token

        Raises:
            AccessTokenServiceError - Unable to generate Access token
        """
        try:
            
            expire = create_UTC_exp_time(
                int(settings.access_token_expire_minutes)
            )
            data = {"user_id": user_id, "exp": expire}

            encoded_jwt = jwt.encode(
                data, 
                settings.secret_key, 
                algorithm=settings.algorithm
            )
            
            return encoded_jwt
        
        except JWTError as e:
            raise AccessTokenServiceError from e
        
        
    
    def create_refresh_token(self, session_id: str) -> tuple[str, datetime]:
        """
        Create refresh token

        Args:
            session_id (int): current session id
        
        Returns:
            tuple[str, datetime]: token a expiration date and time

        Raises:
            RefreshTokenServiceError - Unable to generate token
        """
        try:
            
            expire = create_UTC_exp_time(int(settings.refresh_token_expire_minutes))
            token = secrets.token_hex(int(settings.refresh_token_length))
            
            new_token = RefreshToken(
                session_id=session_id,
                token=token,
                expired_at=expire,
            )
        
            self.repo.create_refresh_token(new_token)
            
            return (token, expire)
        except (
            RefreshTokenCreationError, 
            ValueError, 
            TypeError,
            CreateExecutionError,
        ) as e:
            raise RefreshTokenServiceError("Unable to generate refresh token") from e
            
    
    def create_csrf_token(self) -> str:
        """
        Create csrf token
        
        Returns:
            str: CSRF Token

        Raises:
            CSRFTokenServiceError - unable to generate csrf token
        """
        try:
            return secrets.token_hex(int(settings.csrf_token_length)) 
        except (ValueError, TypeError) as e:
            raise CSRFTokenCreationError from e
    
    def verify_access_token(self, token: str) -> int:
        """
        Verify  access token
        
        Returns:
            int: user id

        Raises:
            AccessTokenServiceError - unable to validate correctly access token
        """
    
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=settings.algorithm,
            )
            
            user_id = payload.get("user_id")
            
            if user_id is None:
                raise AccessTokenServiceError(
                    "Access token does not contain user id"
                ) 
            
            return user_id 
        except JWTError as e:
            raise AccessTokenServiceError("Not valid access token") from e
    
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infrastructure.database.models.auth.refresh_token import RefreshToken
from app.domain.exceptions.repository.token import RefreshTokenCreationError

class TokenRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_refresh_token(self, new_token: RefreshToken):
        """
        Creates a new refresh token.
        
        Args:
            new_token (RefreshToken): The refresh token to create.
            
        Returns:
            RefreshToken: The created refresh token.
            
        Raises:
            RefreshTokenCreationError: If the refresh token already exists.
        """
        try:
            self.db.add(new_token)
            self.db.commit()
        except IntegrityError as e:
            raise RefreshTokenCreationError from e
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.refresh_token import RefreshToken
from app.exceptions.repository.token import RefreshTokenCreationError
from app.exceptions.infrastucture.repository import CreateExecutionError

class TokenRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_refresh_token(self, new_token: RefreshToken):
        try:
            self.db.add(new_token)
            self.db.commit()
        except IntegrityError as e:
            raise RefreshTokenCreationError from e
        except SQLAlchemyError as e:
            raise  CreateExecutionError(
                "Unable to creat refresh token due to server issue"
            ) from e
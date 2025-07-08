from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.token import TokenRepository
from app.services.token import TokenService

class TokenDependencies(TokenService):
    """
    Dependency container for token-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
    ):
        repo = TokenRepository(session)
        
        # business logic
        super().__init__(repo)

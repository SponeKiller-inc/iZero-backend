from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.token import TokenRepository
from app.domain.services.token import TokenService

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

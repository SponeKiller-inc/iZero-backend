from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.token import TokenRepository
from app.services.token import TokenService

class TokenDependencies:
    """
    Dependency container for token-related operations.
    
    Attributes:
        repo (TokenRepository): repository to work with token
        service (TokenService): business logic for token
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
    ):
        repo = TokenRepository(session)
        
        # business logic
        self.service = TokenService(repo)
    
    def __call__(self):
        return self.service
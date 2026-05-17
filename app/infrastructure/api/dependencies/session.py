from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.session import SessionRepository
from app.infrastructure.repositories.token import TokenRepository
from app.domain.entity.session import SessionService
from app.domain.entity.token import TokenService

class SessionDependencies(SessionService):
    """
    Dependency container for session-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
    ):
        session_repo = SessionRepository(session)
        token_repo = TokenRepository(session)
        token_service = TokenService(token_repo)
        
        # business logic
        super().__init__(session_repo, token_service)

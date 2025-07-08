from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.session import SessionRepository
from app.repositories.token import TokenRepository
from app.services.session import SessionService
from app.services.token import TokenService

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

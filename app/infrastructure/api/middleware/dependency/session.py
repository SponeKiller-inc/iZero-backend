from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.session import SessionRepository
from app.infrastructure.repositories.token import TokenRepository
from app.domain.entity.session import SessionService
from app.domain.entity.token import TokenService

class SessionDependencies(SessionService):
    """
    Inicialize Session service
    """

    def __init__(self) -> None:
        self._db_gen = get_db()
        
        # Inicialize db + prepare needed repository and services
        db = next(self._db_gen)
        session_repo = SessionRepository(db)
        token_repo   = TokenRepository(db)
        token_svc    = TokenService(token_repo)

        # Inicialize session service
        super().__init__(session_repo, token_svc)
    
    def __del__(self):
        # End db session
        try:
            next(self._db_gen)       
        except StopIteration:
            pass
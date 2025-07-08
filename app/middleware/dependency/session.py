from app.database.session import get_db
from app.repositories.session import SessionRepository
from app.repositories.token import TokenRepository
from app.services.session import SessionService
from app.services.token import TokenService

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
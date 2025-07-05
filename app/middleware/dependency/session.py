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
        # Inicialize db + prepare needed repository and services
        db_session = get_db()
        session_repo = SessionRepository(db_session)
        token_repo   = TokenRepository(db_session)
        token_svc    = TokenService(token_repo)

        # Inicialize session service
        super().__init__(session_repo, token_svc)

    def __call__(self) -> SessionService:
        return self
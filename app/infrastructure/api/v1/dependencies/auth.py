from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.database.repositories.user import UserRepository
from app.infrastructure.database.repositories.token import TokenRepository
from app.domain.services.auth import AuthService
from app.domain.services.token import TokenService
from app.domain.services.google import GoogleAPI

class AuthDependencies(AuthService):
    """
    Dependency container for auth-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
        google_api: GoogleAPI = Depends(GoogleAPI),
    ):
        #Dependencies
        user_repo = UserRepository(session)
        token_repo = TokenRepository(session)
        token_service = TokenService(token_repo)
        
        super().__init__(user_repo, token_repo, token_service, google_api)
    
from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.user import UserRepository
from app.infrastructure.repositories.token import TokenRepository
from app.domain.entity.auth2 import AuthService
from app.domain.entity.token import TokenService
from app.domain.entity.google import GoogleAPI
from app.infrastructure.services.passlib_password_hasher import PasswordHasher

class AuthDependencies(AuthService):
    """
    Dependency container for auth-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
        google_api: GoogleAPI = Depends(GoogleAPI),
        password_hasher: PasswordHasher = Depends(PasswordHasher),
    ):
        """
        Initializes the AuthDependencies container.
        
        Args:
            session (Session): Database session.
            google_api (GoogleAPI): Google API client.  
            password_hasher (PasswordHasher): Password hashing service.
        """
        #Repositories
        user_repo = UserRepository(session)
        token_repo = TokenRepository(session)
        
        #Services
        token_service = TokenService(token_repo)
        
        super().__init__(user_repo, token_repo, token_service, google_api, password_hasher)
    
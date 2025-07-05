from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user import UserRepository
from app.repositories.token import TokenRepository
from app.services.auth import AuthService
from app.services.token import TokenService
from app.services.google import GoogleAPI

class AuthDependencies:
    """
    Dependency container for auth-related operations.
    
     Attributes:
        service (AuthService): business logic for authorization
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
        
        
        self.service = AuthService(
            user_repo, 
            token_repo, 
            token_service, 
            google_api,
        )
        
    def __call__(self) -> AuthService:
        return self.service    
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.services.google import GoogleAPI

class UserDependencies:
    """
    Dependency container for user-related operations.
    
    Attributes:
        repo (UserRepository): repository to work with user
        service (UserService): business logic for user
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
        google_api: GoogleAPI = Depends(GoogleAPI),
    ):
        repo = UserRepository(session)
        
        # business logic
        self.service = UserService(repo, google_api)
        
    def __call__(self) -> UserService:
        return self.service    
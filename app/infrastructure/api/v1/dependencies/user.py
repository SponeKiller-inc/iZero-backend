from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.user import UserRepository
from app.domain.users.entity.user import UserService
from app.domain.entity.google import GoogleAPI
from app.infrastructure.services.password_hasher import PasswordHasher

class UserDependencies(UserService):
    """
    Dependency container for user-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
        google_api: GoogleAPI = Depends(GoogleAPI),
        password_hasher: PasswordHasher = Depends(PasswordHasher),
    ):
        repo = UserRepository(session)
        super().__init__(repo, google_api, password_hasher)
    
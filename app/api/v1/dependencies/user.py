from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.services.google import GoogleAPI

class UserDependencies(UserService):
    """
    Dependency container for user-related operations.
    """
    def __init__(
        self,
        session: Session = Depends(get_db),
        google_api: GoogleAPI = Depends(GoogleAPI),
    ):
        repo = UserRepository(session)
        super().__init__(repo, google_api)
 

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.services.google import GoogleAPI

def get_user_repo(
    session: Session = Depends(get_db)
) -> UserRepository:
    """
    Managing user data in database

    Args:
        session (Session): SQLAlchemy session provided by `get_db`.

    Returns:
        UserRepository: Repository for performing user data operations.
    """
    return UserRepository(session)

def get_user_service(
    repo: UserRepository = Depends(get_user_repo),
    google_api: GoogleAPI = Depends(GoogleAPI)
) -> UserService:
    """
    Business logic to work with users
    
    Args:
        repo (UserRepository): repository for accessing user data
        google_api (GoogleAPI): client for calling Google APIs

    Returns:
        UserService: services to perform action with users
    """
    return UserService(repo, google_api)
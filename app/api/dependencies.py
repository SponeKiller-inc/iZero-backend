
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

def get_user_repo(
    session: Session = Depends(get_db)
) -> UserRepository:
    return UserRepository(session)

def get_user_service(
    repo: UserRepository = Depends(get_user_repo)
) -> UserService:
    return UserService(repo)
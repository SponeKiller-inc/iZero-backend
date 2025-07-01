from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.sessions import Sessions
from app.exceptions.infrastucture.repository import TokenCreationError

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_session(self, user_id):
        pass
    
    def create_session(self, new_token: Sessions) -> Sessions:
        try:
            self.db.add(new_token)
            self.db.commit()
        except SQLAlchemyError as e:
            raise TokenCreationError("Error while inserting new refresh token to db") from e
    
    def expire_session(self, user_id: int):
        try:
            sessions = (
                self.db
                    .query(Sessions)
                    .filter(Sessions.user_id == user_id)
                    .all()
                )
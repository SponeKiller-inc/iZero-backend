from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class TokenRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_refresh_token(self, user_id):
        pass
    
    def create_refresh_token(self, user_id):
        pass
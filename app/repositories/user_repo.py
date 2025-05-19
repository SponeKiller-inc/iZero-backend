from sqlalchemy.orm import Session

from app.models.users import Users

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def exists_local(self, email: str) -> bool:
        """
        Check if user created locally exists in db 

        Args:
            email (str): user e-mai

        Returns:
            bool: returns True if user exists
        """
        return (
            self.db
                .query(Users)
                .filter(Users.email == email)
                .first() is not None
        )

    def exists_google(self, client_id: str, email: str) -> bool:
        """
        Check if user created via google exists in db

        Args:
            client_id (str): User client_id registered at google
            email (str): user e-mail

        Returns:
            bool: returns True if user exists
        """
        
        is_client_id = (
            self.db
                .query(Users)
                .filter(
                    Users.client_id == client_id,
                    Users.provider == "google"
                )
                .first() is not None
        )
        
        is_email = (
            
        )
                           
        
        
        return (
            self.db
                .query
        )
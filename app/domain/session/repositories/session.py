from typing import Protocol

from app.domain.session.entities.session import Session

class SessionRepository(Protocol):
    def get(self, session_id: int) -> Session | None:
        """
        Get session by ID
        
        Args:
            session_id: Session ID
            
        Returns:
            Session entity if found, else None
        """
        ...

    def get_last_user_session(self, user_id: int) -> Session | None:
        """
        Get last user session by user ID
        
        Args:
            user_id: User ID
            
        Returns:
            Session entity if found, else None
        """
        ...

    def get_by_external_id(self, external_id: str) -> Session | None:
        """
        Get session by external ID
        
        Args:
            external_id: External session ID
            
        Returns:
            Session entity if found, else None
        """
        ...

    def save(self, new_session: Session) -> Session:
        """
        Save session
        
        Args:
            new_session: Session entity to save
            
        Returns:
            Saved Session entity
        """
        ...

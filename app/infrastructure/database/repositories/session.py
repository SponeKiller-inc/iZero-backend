from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infrastructure.database.models.auth.sessions import Sessions
from app.infrastructure.database.models.auth.session_log import SessionLog
from app.infrastructure.utils.utils import create_UTC_exp_time

from app.domain.exceptions.entity.session import (
    SessionCreationError,
    SessionUpdateError,
    SessionLogCreationError,
)

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_last_user_session(self, user_id: int) -> Sessions | None:
        """
        Retrieve data of user session

        Args:
            user_id (int): user e-mail
        
        Returns:
            Sessions or None: session data or None if no data present
        """
        return (
            self.db
                .query(Sessions)
                .filter(Sessions.user_id == user_id)
                .order_by(Sessions.id.desc())
                .first()
            )
        
    def get_session(self, external_id: str) -> Sessions | None:
        """
        Retrieve session data

        Args:
            external_id (str): external session id provided to user
                    
        Returns:
            Sessions or None: session data or None if no data present
        """
        return (
            self.db
                .query(Sessions)
                .filter(
                    Sessions.external_id == external_id,
                )
                .first()
            )

    def create_session(self, new_session: Sessions) -> Sessions:
        """
        Create session

        Args:
            new_session (Sessions) - data tu create session
        
        Returns:
            Sessions: data newly created session
        
        Raises:
            SessionCreationError - invalid data, user doesnt exists
        """
        try:
            self.db.add(new_session)
            self.db.commit()
            self.db.refresh(new_session)
            return new_session
        except IntegrityError as e:
            raise SessionCreationError from e
    
    def expire_session(self, session_id: int) -> None:
        """
        Expire session

        Args:
            new_session (Sessions) - data to create session
        
        Raises:
            SessionUpdateError - invalid session id
            UpdateExecutionError - server side error
        """
        try:
            stmt = (
                self.db
                .query(Sessions)
                .filter(Sessions.id == session_id)
                .update({"expired_at": create_UTC_exp_time(0)})
            )
            self.db.execute(stmt)
            self.db.commit()
        except IntegrityError as e:
            raise SessionUpdateError from e
    
    def create_session_log(self, new_session_log: SessionLog) -> None:
        """
        Create session log

        Args:
            new_session_log (SessionLog) - data to create session log
        
        Raises:
            SessionLogCreationError - invalid session id
            CreateExecutionError - server side error
        """
        
        try:
            self.db.add(new_session_log)
            self.db.commit()
        except IntegrityError as e:
            raise SessionLogCreationError from e
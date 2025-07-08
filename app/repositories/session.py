from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.sessions import Sessions
from app.models.session_log import SessionLog
from app.utils.utils import create_UTC_exp_time

from app.exceptions.repository.session import (
    SessionCreationError,
    SessionUpdateError,
    SessionLogCreationError,
)
from app.exceptions.infrastucture.repository import (
    QueryExecutionError,
    CreateExecutionError,
    UpdateExecutionError,
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
        
        Raises:
            QueryExecutionError: IF any issue on server side
        """
        try:
            return (
                self.db
                    .query(Sessions)
                    .filter(Sessions.user_id == user_id)
                    .order_by(Sessions.id.desc())
                    .first()
                )
        except SQLAlchemyError:
            raise QueryExecutionError("Unable to find user session, db issue")
    def get_session(self, external_id: str) -> Sessions | None:
        """
        Retrieve session data

        Args:
            external_id (str): external session id provided to user
                    
        Returns:
            Sessions or None: session data or None if no data present
        
        Raises:
            QueryExecutionError: IF any issue on server side
        """
        try:
            return (
                self.db
                    .query(Sessions)
                    .filter(
                        Sessions.external_id == external_id,
                    )
                    .first()
                )
        except SQLAlchemyError:
            raise QueryExecutionError("Unable to find session, db issue")
    
    def create_session(self, new_session: Sessions) -> Sessions:
        """
        Create session

        Args:
            new_session (Sessions) - data tu create session
        
        Returns:
            Sessions: data newly created session
        
        Raises:
            SessionCreationError - invalid data, user doesnt exists
            CreateExecutionError - server-side error
        """
        try:
            self.db.add(new_session)
            self.db.commit()
            self.db.refresh(new_session)
            return new_session
        except IntegrityError as e:
            raise SessionCreationError from e
        except SQLAlchemyError:
            raise CreateExecutionError("Unable to create session, db issue")
    
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
        except SQLAlchemyError:
            raise UpdateExecutionError("Unable to expire session, db issue")
    
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
        except SQLAlchemyError:
            raise CreateExecutionError("Unable to create session log, db issue")
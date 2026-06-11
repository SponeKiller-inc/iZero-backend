from sqlalchemy.orm import Session as SqlAlchemySession
from sqlalchemy.exc import IntegrityError

from app.domain.session.entities.session import Session
from app.infrastructure.models.auth.sessions import SessionModel

class AlchemySessionRepository:
    def __init__(self, db: SqlAlchemySession):
        self.db = db

    def get(self, session_id: int) -> Session | None:
        """
        Retrieve session data

        Args:
            session_id (int): session id
                    
        Returns:
            Session or None: session data or None if no data present
        """
        session_model = (
            self.db
                .query(SessionModel)
                .filter(SessionModel.id == session_id)
                .first()
            )
            
        if session_model is None:
            return None

        return Session(
            id=session_model.id,
            external_id=session_model.external_id,
            validity=session_model.validity,
            user_id=session_model.user_id,
            ip_address=session_model.ip_address,
            user_agent=session_model.user_agent 
        )
    
    def get_last_user_session(self, user_id: int) -> Session | None:
        """
        Retrieve data of user session

        Args:
            user_id (int): user e-mail
        
        Returns:
            Session or None: session data or None if no data present
        """
        session = (
            self.db
                .query(SessionModel)
                .filter(SessionModel.user_id == user_id)
                .order_by(SessionModel.id.desc())
                .first()
            )
        
        if session is None:
            return None

        return Session(
            id=session.id,
            external_id=session.external_id,
            validity=session.validity,
            user_id=session.user_id,
            ip_address=session.ip_address,
            user_agent=session.user_agent 
        )
        
    def get_by_external_id(self, external_id: str) -> Session | None:
        """
        Retrieve session data

        Args:
            external_id (str): external session id provided to user
                    
        Returns:
            Session or None: session data or None if no data present
        """

        session = (
            self.db
                .query(SessionModel)
                .filter(
                    SessionModel.external_id == external_id,
                )
                .first()
        )

        if session is None:
            return None

        return Session(
            id=session.id,
            external_id=session.external_id,
            validity=session.validity,
            user_id=session.user_id,
            ip_address=session.ip_address,
            user_agent=session.user_agent 
        )
    
    def save(self, session: Session) -> Session:
        """
        Create or update session

        Args:
            session (Session): data to create or update session
        
        Returns:
            Session: data newly created or updated session
        """
         
        if session.id is None:
            return self._insert(session)
        else:
            return self._update(session)

    def _insert(self, session: Session) -> Session:
        """
        Create session

        Args:
            session (Session) - data tu create session
        
        Returns:
            Session: data newly created session
        """
               
        session_model = SessionModel(
            external_id=session.external_id,
            validity=session.validity,
            user_id=session.user_id,
            ip_address=session.ip_address,
            user_agent=session.user_agent 
        )
        self.db.add(session_model)
        self.db.commit()
        self.db.refresh(session_model)

        return Session(
            id=session_model.id,
            external_id=session_model.external_id,
            validity=session_model.validity,
            user_id=session_model.user_id,
            ip_address=session_model.ip_address,
            user_agent=session_model.user_agent 
        )

    def _update(self, session: Session) -> Session:
        """
        Update session

        Args:
            session (Session) - data to update session
        
        Returns:
            Session: data updated session
        """

        updated_session = (
            self.db
                .query(SessionModel)
                .filter(SessionModel.id == session.id)
                .first()      
        )

        updated_session.external_id = session.external_id
        updated_session.validity = session.validity
        updated_session.user_id = session.user_id
        updated_session.ip_address = session.ip_address
        updated_session.user_agent = session.user_agent

        self.db.commit()
        self.db.refresh(updated_session)

        return Session(
            id=updated_session.id,
            external_id=updated_session.external_id,
            validity=updated_session.validity,
            user_id=updated_session.user_id,
            ip_address=updated_session.ip_address,
            user_agent=updated_session.user_agent 
        )
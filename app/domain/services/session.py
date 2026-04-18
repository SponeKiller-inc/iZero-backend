import uuid

from app.domain.repository.session import ISessionRepository
from app.domain.services.token import TokenService
from app.infrastructure.database.models.auth.sessions import Sessions
from app.infrastructure.database.models.auth.session_log import SessionLog
from app.domain.exceptions.entity.session import (
    SessionCreationError,
    SessionUpdateError,
    SessionLogCreationError,
    LogSessionServiceError,
    UserSessionServiceError,
    InicializeSessionServiceError,
    GetSessionServiceError,
)
from app.domain.exceptions.entity.token import AccessTokenServiceError

from app.infrastructure.utils.config import settings
from app.infrastructure.utils.utils import create_UTC_exp_time, get_UTC_current_time

class SessionEventType:
    SESSION_INITIALIZED   = "session_initialized"
    SESSION_RESUMED       = "session_resumed"
    PAGE_VIEW             = "page_view"
    API_CALL              = "api_call"
    USER_LOGGED_IN        = "user_logged_in"
    USER_LOGGED_OUT       = "user_logged_out"
    SESSION_EXPIRED       = "session_expired"
    
class SessionService:
    def __init__(
        self, 
        repo: ISessionRepository,
        token_service: TokenService
    ):
        self.repo = repo
        self.token_service = token_service
        
    def inicialize_session(
        self, 
        external_id: str, 
        jwt_token: str, 
        ip_address: str, 
        user_agent: str,
    ) -> tuple[int, str]:
        """
        Inicialize session
        (validate current session if not OK, create new)

        Args:
            external_id (str): session id provided to user
            jwt_token (str): jwt acces token with user id
            ip_address (str): user ip_address
            user_agent (str): user agent from http header
        
        Returns:
            int: current user session
        
        Raises:
            InicializeSessionServiceError: issue while inicializing session
        """
        
        try:
            if jwt_token: 
                # User logged in
                user_id = self.token_service.verify_access_token(jwt_token)
            else:
                user_id = None
                
            # Clean up previous user session
            if (
                external_id is None and 
                user_id is not None and
                user_id > 0
            ):
                # session not exist bud we know user
                session = self.repo.get_last_user_session(user_id)
                if session.expired_at > get_UTC_current_time():
                    # expire last user session if not expired
                    self.repo.expire_session(session.id)
            
            if external_id is not None:
                # Verify session
                session = self.repo.get_session(external_id)
                
                if session is None:
                    # Not valid = as it did not existed
                    external_id = 0
            
            if external_id is None:
                # Create new session
                session = self._create_session(user_id, ip_address, user_agent)
        except (
            AccessTokenServiceError,
            UserSessionServiceError, 
            SessionUpdateError,
            QueryExecutionError,
            UpdateExecutionError,
        ) as e:
            raise InicializeSessionServiceError from e
        
        return (session.id, session.external_id)
        
    def _create_session(
        self, 
        user_id: int,
        ip_address: str,
        user_agent: str,
    ) -> Sessions:
        """
        Create session

        Args:
            user_id (int): user id
            ip_address (str): user ip_address
            user_agent (str): user agent from http header
        
        Returns:
            Sessions: created session
        
        Raises:
            UserSessionServiceError: issue while creating new session
        """
        
        try:
            expired_at = create_UTC_exp_time(
                int(settings.session_expire_minutes)
            )
            
            new_session = Sessions(
                external_id=uuid.uuid4(),
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                expired_at=expired_at,
            )
            
            # Create new session
            return self.repo.create_session(new_session)
        except (
            SessionCreationError,
            CreateExecutionError,
        ) as e:
            raise UserSessionServiceError from e
    
    def record_session_event(
        self, 
        session_id: int, 
        event_type: str, 
    ) -> None:
        """
        Records session event

        Args:
            session_id (int): session id
            event_type (str): which resources user asked    
        
        Raises:
            LogSessionServiceError: issue while inserting session record
        """

        try:
            new_session_log = SessionLog(
                session_id=session_id,
                event_type=event_type
            )
            self.repo.create_session_log(new_session_log)
        except (
            SessionLogCreationError,
            CreateExecutionError,
        ) as e:
            raise LogSessionServiceError from e
    
    def retrieve_session(self, external_id: str) -> Sessions:
        """
        Retrieve session

        Args:
            external_id (str): session id provided to user
        
        Returns:
            Sessions: session data
        """
        
        return self.repo.get_session(external_id)
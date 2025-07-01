import secrets

from jose import JWTError, jwt
from datetime import datetime

from app.repositories.session import SessionRepository
from app.models.sessions import Sessions
from app.models.session_log import SessionLog
from app.exceptions.repository.session import (
    SessionCreationError,
    SessionUpdateError,
)
from app.exceptions.infrastucture.repository import (
    CreateExecutionError,
    UpdateExecutionError,
)
from app.exceptions.domain.session import (
    LogSessionServiceError,
    UserSessionServiceError,
)

from app.utils.config import settings
from app.utils.utils import create_UTC_exp_time
from app.utils.validation import validate_positive_int
class SessionService:
    def __init__(
        self, 
        repo: SessionRepository,
    ):
        self.repo = repo
    
    def create_user_session(
        self, 
        user_id: int,
        ip_adress: str,
        user_agent: str,
        metadata: dict,
    ) -> int:
        
        try:
            # Invalidate all current user session
            self.repo.expire_session(user_id)
            
            expire = create_UTC_exp_time(
                int(settings.session_expire_minutes)
            )
            
            new_session = Sessions(
                user_id=user_id,
                ip_adress=ip_adress,
                user_agent=user_agent,
                expired_at=expire,
                metadata=metadata,
            )
            # Create new session
            session = self.repo.create_session(new_session)
            
            return session.id
        except (
            SessionUpdateError, 
            SessionCreationError,
            UpdateExecutionError,
            CreateExecutionError,
        ) as e:
            raise UserSessionServiceError from e
    
    def create_session_log(
        self, 
        session_id: int, 
        event_type: str, 
        metadata: dict
    ):
        try:
            pass
        except (
            SessionLogCreationError,
            CreateExecutionError,
        ) as e:
            raise
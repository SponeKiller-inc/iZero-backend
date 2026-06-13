from app.application.ports.time_provider import TimeProvider
from app.application.constants.session import SessionConstants
from app.application.dto.sessions.inicialize_session import (
    InitializeSessionIn,
    InicializeSessionOut,
)
from app.application.exceptions.user import UserNotFoundError
from app.domain.session.entities.session import Session
from app.domain.session.repositories.session import SessionRepository
from app.domain.users.repositories.user import UserRepository

class InicializeSession:

    def __init__(
        self,
        session_repository: SessionRepository,
        user_repository: UserRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initializes a new session.

        Args:
            session_repository (SessionRepository): The session repository.
            user_repository (UserRepository): The user repository.
            time_provider (TimeProvider): The time provider.
        """
        self.session_repository = session_repository
        self.user_repository = user_repository
        self.time_provider = time_provider

    def execute(self, dto: InitializeSessionIn) -> InicializeSessionOut:
        """
        Initializes a new session.

        Args:
            dto (InitializeSessionIn): The session data.

        Returns:
            Session: data newly created or updated session
        
        Raises:
            UserNotFoundError: user with such id doesn't exist
        """
        # 1. Check if user exists
        if dto.user_id > 0:
            user_exists = self.user_repository.exists_user(dto.user_id)

            if not user_exists:
                raise UserNotFoundError
        

        # 2. Check if session is not expired
        if dto.external_id > 0:
            session = self.session_repository.get_by_external_id(dto.external_id)

            if session and not session.is_expired(self.time_provider):
                return session

        # 3. Invalidate user last session 
        if dto.user_id > 0:
            last_session = self.session_repository.get_last_user_session(dto.user_id)
            if last_session is not None:
                last_session.expire_now(self.time_provider)
                self.session_repository.update(last_session)

        # 4. Create new a return 
        session = Session.create_new(
            dto.user_id,
            dto.ip_address,
            dto.user_agent,
            self.time_provider.get_expiration(
                SessionConstants.SESSION_EXPIRATION_MINUTES,
            ),
            self.time_provider.now(),
        )
        
        session = self.session_repository.save(session)
        
        return InicializeSessionOut(session.external_id)
        
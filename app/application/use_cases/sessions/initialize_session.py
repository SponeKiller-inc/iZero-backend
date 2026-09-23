from app.application.constants.session import SessionConstants
from app.application.dto.sessions.initialize_session import (
    InitializeSessionIn,
    InitializeSessionOut,
)
from app.application.exceptions.user import UserNotFoundError
from app.application.ports.time_provider import TimeProvider
from app.domain.session.entities.session import Session
from app.domain.session.repositories.session import SessionRepository
from app.domain.users.repositories.user import UserRepository


class InitializeSession:

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

    def execute(self, dto: InitializeSessionIn) -> InitializeSessionOut:
        """
        Initializes a new session.

        Args:
            dto (InitializeSessionIn): The session data.

        Returns:
            Session: data newly created or updated session
        
        Raises:
            UserNotFoundError: user with such id doesn't exist
        """
        has_user = dto.user_id is not None and dto.user_id > 0

        # 1. Check if user exists
        if has_user:
            user = self.user_repository.get(dto.user_id)

            if user is None:
                raise UserNotFoundError
        

        # 2. Check if session is not expired
        if dto.external_id:
            session = self.session_repository.get_by_external_id(dto.external_id)

            if session and not session.is_expired(self.time_provider.now()):
                # Covers both switching to another user and logging out of one;
                # in both cases the session bound to the old user is now stale.
                user_changed = session.user_id is not None and session.user_id != dto.user_id

                if user_changed:
                    session.expire_now(self.time_provider.now())
                    self.session_repository.save(session)
                elif session.user_id is None and has_user:
                    # Only fill in the user on a still-anonymous session.
                    session.assign_user(dto.user_id, self.time_provider.now())
                    session = self.session_repository.save(session)

                if not user_changed:
                    return InitializeSessionOut(session.id, session.external_id)

        # 3. Invalidate user last session 
        if has_user:
            last_session = self.session_repository.get_last_user_session(dto.user_id)
            if last_session is not None:
                last_session.expire_now(self.time_provider.now())
                self.session_repository.save(last_session)

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
        
        return InitializeSessionOut(session.id, session.external_id)
        
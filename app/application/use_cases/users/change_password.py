from app.application.constants.use_case import UseCase
from app.application.dto.user.change_password import ChangePasswordIn
from app.application.exceptions.user import (
    InvalidCurrentPasswordError,
    PasswordChangeNotSupportedError,
    PasswordConfirmationMismatchError,
    PasswordSameAsCurrentError,
    PasswordTooLongError,
    PasswordTooShortError,
    UserNotFoundError,
)
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.domain.session.constants.session_event import SessionEventType
from app.domain.session.repositories.session import SessionRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.exceptions import user as user_errors
from app.domain.users.repositories.user import UserRepository
from app.domain.users.value_objects.password import Password


class ChangePassword:

    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        password_hasher: PasswordHasher,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_repository: User repository
            session_repository: Session repository
            password_hasher: Password hasher
            time_provider: Time provider
        """
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.password_hasher = password_hasher
        self.time_provider = time_provider

    @authorize(EntityType.USERS, UseCase.USERS_CHANGE_PASSWORD)
    def execute(self, dto: ChangePasswordIn) -> None:
        """
        Changes password of the given user. The current session stays valid
        and records the password change event.

        Args:
            dto: DTO carrying user id, current password, new password, its confirmation
                and the current session id.

        Raises:
            UserNotFoundError: If user does not exist
            PasswordChangeNotSupportedError: If user account has no password
            InvalidCurrentPasswordError: If current password is wrong
            PasswordTooShortError: If new password is too short
            PasswordTooLongError: If new password is too long
            PasswordConfirmationMismatchError: If confirmation differs from new password
            PasswordSameAsCurrentError: If new password equals the current one
        """

        now = self.time_provider.now()
        user = self.user_repository.get(dto.user_id)

        if user is None:
            raise UserNotFoundError("User not found")

        current_session = self.session_repository.get(dto.session_id)

        if not user.has_password():
            raise PasswordChangeNotSupportedError("User has no password to change")

        if not self.password_hasher.verify(dto.current_password, user.password):
            raise InvalidCurrentPasswordError("Current password is invalid")

        try:
            new_password = Password(dto.new_password)
        except user_errors.PasswordTooShortError as e:
            raise PasswordTooShortError from e
        except user_errors.PasswordTooLongError as e:
            raise PasswordTooLongError from e

        if dto.password_confirmation != new_password.value:
            raise PasswordConfirmationMismatchError(
                "Password confirmation does not match the new password"
            )

        if self.password_hasher.verify(new_password.value, user.password):
            raise PasswordSameAsCurrentError("New password is the same as the current one")

        # Changing password
        user.change_password(self.password_hasher.hash(new_password.value))
        self.user_repository.save(user)

        current_session.record_event(SessionEventType.PASSWORD_CHANGED, now)
        self.session_repository.save(current_session)

from app.application.constants.use_case import UseCase
from app.application.exceptions.user import (
    UserCannotBeDeletedError,
    UserDeleteForbiddenError,
    UserNotFoundError,
)
from app.application.security.auth_context import AuthContext
from app.application.security.authorize import authorize
from app.domain.shared.constants.entity_type import EntityType
from app.domain.users.exceptions.user import UserInactiveError, UserProtectedError
from app.domain.users.repositories.user import UserRepository


class DeleteUser:

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_repository: User repository
        """
        self.user_repository = user_repository

    @authorize(EntityType.USERS, UseCase.USERS_DELETE)
    def execute(self, user_id: int) -> None:
        """
        Soft delete user by setting it inactive

        Args:
            user_id: ID of the user to delete

        Raises:
            UserDeleteForbiddenError: If caller tries to delete another user
            UserNotFoundError: If user does not exist or is already deleted
            UserCannotBeDeletedError: If user is the bootstrap admin
        """
        # Self-service only, checked before lookup so foreign ids can't be probed
        if AuthContext.get() != user_id:
            raise UserDeleteForbiddenError("You can delete only your own account")

        user = self.user_repository.get(user_id)

        if user is None:
            raise UserNotFoundError("User not found")

        try:
            user.deactivate()
        except UserInactiveError:
            raise UserNotFoundError("User not found")
        except UserProtectedError:
            raise UserCannotBeDeletedError("User cannot be deleted")

        self.user_repository.save(user)

from app.application.constants.use_case import UseCase
from app.application.exceptions.user import UserCannotBeDeletedError, UserNotFoundError
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
            UserNotFoundError: If user does not exist or is already deleted
            UserCannotBeDeletedError: If user is the bootstrap admin or the caller
        """
        user = self.user_repository.get(user_id)

        if user is None:
            raise UserNotFoundError("User not found")

        try:
            user.deactivate(actor_id=AuthContext.get())
        except UserInactiveError:
            raise UserNotFoundError("User not found")
        except UserProtectedError:
            raise UserCannotBeDeletedError("User cannot be deleted")

        self.user_repository.save(user)

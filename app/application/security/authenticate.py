from app.application.exceptions.auth import UnauthenticatedUserError
from app.application.exceptions.user import UserModuleNotAssignedError
from app.application.ports.time_provider import TimeProvider
from app.domain.users.entities.user_module import UserModule
from app.domain.shared.value_objects.period import ValidityPeriod
from app.domain.users.repositories.user_role import UserRoleRepository
from app.application.security.auth_context import AuthContext
from app.application.security.hash_context import HashContext
from app.application.security.secret_message_context import SecretMessageContext
from app.application.constants.security import SecurityConstants
from app.domain.shared.value_objects.role import Role

class Authenticate:

    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            user_role_repository: User role repository
            time_provider: Time provider
        """
        self.user_role_repository = user_role_repository
        self.time_provider = time_provider
        
    def execute(self, user_id: int) -> None:
        """
        Assign module to user

        Args:
            user_id: User ID
        """

        current_user_id = AuthContext.get()

        if current_user_id is None:
            raise UnauthenticatedUserError("You are not authenticated")

        if current_user_id != user_id:
            raise UnauthenticatedUserError(
            "You dont have permission to access this user"
            )

        # 1. 
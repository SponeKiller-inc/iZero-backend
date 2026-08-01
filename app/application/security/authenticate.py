from app.domain.auth.repositories.role_permission import RolePermissionRepository
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
        role_permission_repository: RolePermissionRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            user_role_repository: User role repository
            role_permission_repository: Role permission repository
            time_provider: Time provider
        """
        self.user_role_repository = user_role_repository
        self.role_permission_repository = role_permission_repository
        self.time_provider = time_provider
        
    def execute(self, user_id: int) -> None:
        """
        Assign module to user

        Args:
            user_id: User ID of who is accessing resource 
        """

        current_user_id = AuthContext.get()

        if current_user_id is None:
            raise UnauthenticatedUserError("You are not authenticated")

        if current_user_id != user_id:
            raise UnauthenticatedUserError(
            "You dont have permission to access this user"
            )

        # 1. Zjistíme z user_id roli 
        # 2. Podle role dohledá aktivní přístupy k jakým zdrojům
        # 3. vytvoříme k ním pole hashu
        # 4. Hashe uložíme do globálního kontextu 


        user_roles = self.user_role_repository.get(user_id, self.time_provider.now())

        for user_role in user_roles:
            self.role_permission_repository.get(user_role.role_id, self.time_provider.now())
        
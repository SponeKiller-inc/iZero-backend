from app.application.constants.security import SecurityConstants
from app.application.exceptions.auth import UnauthenticatedUserError
from app.application.ports.time_provider import TimeProvider
from app.application.security.auth_context import AuthContext
from app.application.security.auth_hash import AuthHash
from app.application.security.hash_context import HashContext
from app.application.security.secret_message_context import (
    SecretMessageContext,
)
from app.domain.auth.repositories.role_permission import (
    RolePermissionRepository,
)
from app.domain.users.repositories.user_role import UserRoleRepository


class Authenticate:
    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        role_permission_repository: RolePermissionRepository,
        time_provider: TimeProvider,
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
        Authenticate user and set hash context

        Args:
            user_id: User id
        
        Raises:
            UnauthenticatedUserError: If user is not authenticated
        """

        if user_id is None:
            raise UnauthenticatedUserError("You are not authenticated")

        auth_hash = AuthHash(SecurityConstants.AUTH_SECRET)
        entities_methods: list[tuple[str, str]] = []

        user_roles = self.user_role_repository.get(
            user_id,
            self.time_provider.now(),
        )

        # Generate hashes for every use-case, that user can access
        for user_role in user_roles:
            role_permissions = self.role_permission_repository.get(
                user_role.role_id,
                self.time_provider.now(),
            )
            for role_permission in role_permissions:
                entities_methods.append((
                    role_permission.permission_code.entity.type.value,
                    role_permission.permission_code.method,
                ))

        hashes = auth_hash.generate(
            AuthContext.get(),
            SecretMessageContext.get(),
            entities_methods,
        )

        HashContext.set(hashes)
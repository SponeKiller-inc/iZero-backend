from app.application.security.authorize import authorize
from app.application.exceptions.user import UserModuleNotAssignedError
from app.application.exceptions.module import ModuleNotFoundError
from app.domain.users.repositories.user_module import UserModuleRepository
from app.application.ports.time_provider import TimeProvider
from app.application.dto.user.assign_module import AssignModuleIn
from app.domain.modules.repositories.module import ModuleRepository
from app.domain.users.entities.user_module import UserModule
from app.domain.shared.value_objects.period import ValidityPeriod
from app.application.constants.use_case import UseCase
from app.domain.shared.constants.entity_type import EntityType

class AssignModule:

    def __init__(
        self,
        module_repository: ModuleRepository,
        user_module_repository: UserModuleRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            module_repository: Module repository
            user_module_repository: User module repository
            time_provider: Time provider
        """
        self.module_repository = module_repository
        self.user_module_repository = user_module_repository
        self.time_provider = time_provider

    @authorize(EntityType.USERS, UseCase.USERS_ASSIGN_MODULE)
    def execute(self, dto: AssignModuleIn) -> None:
        """
        Assign module to user

        Args:
            dto: DTO carrying user data from any identity provider.
        
        Raises:
            UserModuleNotAssignedError: If user already exists
        """
        # Validation
        now = self.time_provider.now()
        expiration = self.time_provider.get_expiration(days=dto.duration_days)
        module = self.module_repository.get(dto.module_id, now)

        if module is None:
            raise ModuleNotFoundError("Module does not exist")

        if not module.is_active(now):
            raise UserModuleNotAssignedError("Module is not active")

        if not module.is_active(expiration):
            raise UserModuleNotAssignedError(
                "Module will not be valid at the end of the validity period"
            )

        user_modules = self.user_module_repository.get(dto.user_id, now)
        
        validity = ValidityPeriod(
            valid_from=now,
            valid_to=expiration
        )

        for user_module in user_modules:
            if validity.overlaps_with(user_module.validity):
                raise UserModuleNotAssignedError(
                    "Module already assigned to user in overlapping period"
                )

        # Assigning module to suer
        user_module = UserModule.assign(
            user_id=dto.user_id,
            module_id=dto.module_id,
            validity=validity
        )

        self.user_module_repository.save(user_module)
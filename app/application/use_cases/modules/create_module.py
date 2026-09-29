from app.application.constants.use_case import UseCase
from app.application.dto.module.create_module import CreateModuleIn, CreateModuleOut
from app.application.exceptions.module import ModuleGroupNotFoundError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.domain.modules.entities.module import Module
from app.domain.modules.repositories.module import ModuleRepository
from app.domain.modules.repositories.module_group import ModuleGroupRepository
from app.domain.shared.constants.entity_type import EntityType


class CreateModule:

    def __init__(
        self,
        module_repository: ModuleRepository,
        module_group_repository: ModuleGroupRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize use-case

        Args:
            module_repository: Module repository
            module_group_repository: Module group repository
            time_provider: Time provider
        """
        self.module_repository = module_repository
        self.module_group_repository = module_group_repository
        self.time_provider = time_provider

    @authorize(EntityType.MODULES, UseCase.MODULES_CREATE)
    def execute(self, dto: CreateModuleIn) -> CreateModuleOut:
        """
        Create new module

        Args:
            dto: Module data

        Returns:
            Created module

        Raises:
            ModuleGroupNotFoundError: If module group does not exist
        """
        now = self.time_provider.now()
        module_group = self.module_group_repository.get(dto.module_group_id, now)

        if module_group is None:
            raise ModuleGroupNotFoundError("Module group does not exist")

        module = Module.create(dto.name, dto.module_group_id, dto.valid_from)
        module = self.module_repository.save(module)

        return CreateModuleOut(
            id=module.id,
            name=module.name,
            module_group_id=module.module_group_id,
            valid_from=module.validity.valid_from,
            valid_to=module.validity.valid_to,
        )

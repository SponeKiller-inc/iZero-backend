from app.application.ports.time_provider import TimeProvider
from app.application.dto.module.create_module_group import CreateModuleGroupIn, CreateModuleGroupOut
from app.application.security.authorize import authorize
from app.application.constants.use_case import UseCase
from app.domain.modules.repositories.module_group import ModuleGroupRepository
from app.domain.modules.entities.module_group import ModuleGroup
from app.domain.shared.constants.entity_type import EntityType


class CreateModuleGroup:

    def __init__(
        self,
        module_group_repository: ModuleGroupRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize use-case

        Args:
            module_group_repository: Module group repository
            time_provider: Time provider
        """
        self.module_group_repository = module_group_repository
        self.time_provider = time_provider

    @authorize(EntityType.MODULES, UseCase.MODULES_CREATE_GROUP)
    def execute(self, dto: CreateModuleGroupIn) -> CreateModuleGroupOut:
        """
        Create new module group

        Args:
            dto: Module group data

        Returns:
            Created module group
        """
        module_group = ModuleGroup.create(dto.name, dto.valid_from)
        module_group = self.module_group_repository.save(module_group)

        return CreateModuleGroupOut(
            id=module_group.id,
            name=module_group.name,
            valid_from=module_group.validity.valid_from,
            valid_to=module_group.validity.valid_to,
        )

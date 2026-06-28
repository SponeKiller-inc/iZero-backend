from app.application.ports.time_provider import TimeProvider
from app.application.dto.user.retrieve_modules import RetrieveModulesOut, ModuleDto
from app.domain.users.repositories.user_module import UserModuleRepository
from app.domain.modules.repositories.module import ModuleRepository
from app.domain.modules.repositories.module_group import ModuleGroupRepository

class RetrieveModules:

    def __init__(
        self,
        user_module_repository: UserModuleRepository,
        module_repository: ModuleRepository,
        module_group_repository: ModuleGroupRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            user_module_repository: User module repository
            module_repository: Module repository
            module_group_repository: Module group repository
            time_provider: Time provider
        """
        self.user_module_repository = user_module_repository
        self.module_repository = module_repository
        self.module_group_repository = module_group_repository
        self.time_provider = time_provider
        
    def execute(self, user_id: int) -> list[RetrieveModulesOut]:
        """
        Retrieve modules for user

        Args:
            user_id: User ID

        Returns:
            List of RetrieveModulesOut objects
        """

        result: list[RetrieveModulesOut] = []

        user_modules = self.user_module_repository.get(user_id, self.time_provider.now())       

        for user_module in user_modules:
            module = self.module_repository.get(user_module.module_id)
            module_group = self.module_group_repository.get(module.module_group_id)

            for module_group in result:
                if module_group.module_group_id == module.module_group_id:
                    module_group.modules.append(ModuleDto(
                        id=user_module.module_id,
                        name=module.name,
                    ))
                    break
            else:
                result.append(
                    RetrieveModulesOut(
                        module_group_id=module_group.id,
                        module_group_name=module_group.name,
                        modules=[ModuleDto(
                            id=module.id,
                            name=module.name,
                        )],
                    )
                )

        return result
        
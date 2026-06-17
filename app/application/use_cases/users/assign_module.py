from app.domain.users.entities.user_module import UserModule
from app.application.exceptions.user import UserModuleNotAssignedError
from app.domain.users.repositories.user_module import UserModuleRepository
from app.application.ports import time_provider
from app.application.ports.time_provider import TimeProvider
from app.application.ports.password_hasher import PasswordHasher
from app.application.dto.user.assign_module import AssignModuleIn
from app.application.exceptions.user import RegisterLocalError
from app.domain.users.repositories.user import UserRepository
from app.domain.users.entities.user import User
from app.domain.users.exceptions.user import UserValidationError
from app.domain.modules.repositories.module import ModuleRepository

class AssignModule:

    def __init__(
        self,
        user_repository: UserRepository,
        module_repository: ModuleRepository,
        user_module_repository: UserModuleRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            user_repository: User repository
            module_repository: Module repository
            user_module_repository: User module repository
            time_provider: Time provider
        """
        self.user_repository = user_repository
        self.module_repository = module_repository
        self.user_module_repository = user_module_repository
        self.time_provider = time_provider
        
    def execute(self, dto: AssignModuleIn) -> None:
        """
        Assign module to user

        Args:
            dto: DTO carrying user data from any identity provider.
        
        Raises:
            UserModuleNotAssignedError: If user already exists
        """
        # 1. Ověříme že modul existuje
        module = self.module_repository.get(dto.module_id)

        # 2. Zkontroluje zda je aktivní modul
        if not module.is_active(self.time_provider.now()):
            raise UserModuleNotAssignedError("Module is not active")

        # 3. Vytvoříme entitu user_module
        user_module = UserModule(
            user_id=dto.user_id,
            module_id=dto.module_id,
            assigned_at=self.time_provider.now()
        )

        # 4. Uložíme do databáze 

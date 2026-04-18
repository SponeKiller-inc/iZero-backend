from abc import ABC, abstractmethod
from datetime import datetime

from app.models.user_modules import UserModules
from app.models.modules import Modules
from app.models.module_groups import ModuleGroups

class IModuleRepository(ABC):
    @abstractmethod
    def get_user_modules(self, user_id: int) -> dict[str, list[str]] | None:
        pass

    @abstractmethod
    def is_active_user_module(
        self, 
        user_id: int, 
        module_id: int,
        valid_from: datetime,
        valid_to: datetime,
    ) -> bool:
        pass

    @abstractmethod
    def add_user_module(self, new_user_module: UserModules) -> UserModules:
        pass

    @abstractmethod
    def add_module_group(self, new_module_group: ModuleGroups) -> ModuleGroups:
        pass

    @abstractmethod
    def add_module(self, new_module: Modules) -> Modules:
        pass

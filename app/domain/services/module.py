from datetime import datetime

from app.infrastructure.database.models.module.user_modules import UserModules
from app.infrastructure.database.models.module.module_groups import ModuleGroups
from app.infrastructure.database.models.module.modules import Modules
from app.domain.repository.module import IModuleRepository
from app.domain.exceptions.entity.module import (
    UserModuleNotFoundError, 
    UserModuleNotAssignedError,
    ModuleGroupNotCreatedError,
    ModuleNotCreatedError,
)
from app.domain.exceptions.repository.module import (
    UserModuleNotAddedError,
    ModuleGroupNotAddedError,
    ModuleNotAddedError,
)
from app.infrastructure.utils import utils
from app.infrastructure.utils.config import settings
class ModuleService:
    def __init__(
        self, 
        module_repo: IModuleRepository, 
    ):
        self.module_repo = module_repo
        
    def retrieve_user_modules(self, user_id: int) -> dict[str, list[str]]:
        
        """
        Retrieves available user modules 

        Args:
            user_id (int): user id

        Returns:
            dict[str, list[str]]: data of user modules 
                (ModuleGroup: list of modules)
        
        Raises:
            UserModuleNotFoundError: No module found 
        """

        data = self.module_repo.get_user_modules(user_id)
        
        if data is None:
            raise UserModuleNotFoundError
        
        return data
        
    def assign_module_to_user(
        self, 
        user_id: int, 
        module_id: int,
        valid_from: datetime | None = None,
        valid_to: datetime | None = None,
    ) -> None:
        """
        Add new module to user

        Args:
            user_id (int): user id
            module_id (int): module id which is added
            valid_from (datetime): date and time valid from 
                if None, set current time
            valid_from (datetime): date and time valid to
                if None, set value base of env variable
        
        Raises:
            UserModuleNotAssignedError: Invalid data or service module  not exists 
                or module active
        """
        
        if valid_from is None:
            valid_from = utils.get_UTC_current_time()
            
        if valid_to is None:
            valid_to = utils.create_UTC_exp_time(settings.user_module_expire_minutes)
        
        if self.module_repo.is_active_user_module(
            user_id,
            module_id, 
            valid_from, 
            valid_to,
        ):
            raise UserModuleNotAssignedError(
                "Unable to assign module, because is active"
            )
        
        try:
            new_user_module = UserModules(
                user_id=user_id,
                module_id=module_id,
                valid_from=valid_from,
                valid_to=valid_to,
            )
            self.module_repo.add_user_module(new_user_module)
        except UserModuleNotAddedError as e:
            raise UserModuleNotAssignedError from e
        
    def create_module_group(self, module_group_name: str) -> int:
        """
        Create new module group

        Args:
            module_group_name (str): name of module group
        
        Raises:
            ModuleGroupNotCreatedError: Invalid data
        """
        
        try:
            new_module_group = ModuleGroups(name=module_group_name)
            module_group = self.module_repo.add_module_group(new_module_group)
            
            return module_group.id
        except ModuleGroupNotAddedError as e:
            raise ModuleGroupNotCreatedError from e
        
    def create_module(self, module_name: str, module_group_id: int) -> int:
        """
        Create new module

        Args:
            module_name (str): name of module group
            module_group_id (int): id module group to which assign
        
        Raises:
            ModuleNotCreatedError: Invalid data or module group not exists
        """
        
        try:
            new_module = Modules(
                module_group_id=module_group_id,
                name=module_name,
            )
            module = self.module_repo.add_module(new_module)
            
            return module.id
        except ModuleNotAddedError as e:
            raise ModuleNotCreatedError from e
            
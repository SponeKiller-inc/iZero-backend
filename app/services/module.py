from datetime import datetime

from app.utils.config import settings
from app.models.user_modules import UserModules
from app.models.module_groups import ModuleGroups
from app.models.modules import Modules
from app.repositories.module import ModuleRepository
from app.exceptions.domain.module import (
    ModuleNotFoundError, 
    UserModuleNotAssignedError,
    ModuleGroupNotCreatedError,
    ModuleNotCreatedError,
)
from app.exceptions.repository.module import (
    UserModuleNotAddedError,
    ModuleGroupNotAddedError,
    ModuleNotAddedError,
)
from app.exceptions.infrastucture.repository import (
    QueryExecutionError,
    CreateExecutionError,
)
from app.exceptions.infrastucture.domain import ModuleServiceError
from app.utils.utils import get_UTC_current_time, create_UTC_exp_time

class ModuleService:
    def __init__(
        self, 
        module_repo: ModuleRepository, 
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
            ModuleNotFoundError: No module found 
            ModuleServiceError: Something went wrong, while procesing
        """

        try:
            data = self.module_repo.get_user_modules(user_id)
            
            if data is None:
                raise ModuleNotFoundError
            
            return data
        except QueryExecutionError as e:
            raise ModuleServiceError("Unable to retrive user modules") from e
        
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
            ModuleServiceError: Something went wrong, while procesing
        """
        
        if valid_from is None:
            valid_from = get_UTC_current_time()
            
        if valid_to is None:
            valid_to = create_UTC_exp_time(settings.user_module_expire_minutes)
        
        if self.module_repo.is_active_user_module(
            user_id,
            module_id, 
            valid_from, 
            valid_to,
        ):
            raise UserModuleNotAssignedError(
                "Unable to assigne module, because is active"
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
        except CreateExecutionError as e:
            raise ModuleServiceError("Unable to assign module to user") from e
        
    def create_module_group(self, module_group_name: str) -> int:
        """
        Create new module group

        Args:
            module_group_name (str): name of module group
        
        Raises:
            ModuleGroupNotCreatedError: Invalid data
            ModuleServiceError: Something went wrong, while procesing
        """
        
        try:
            new_module_group = ModuleGroups(name=module_group_name)
            module_group = self.module_repo.add_module_group(new_module_group)
            
            return module_group.id
        except ModuleGroupNotAddedError as e:
            raise ModuleGroupNotCreatedError from e
        except CreateExecutionError as e:
            raise ModuleServiceError("Unable to create module group")
        
    def create_module(self, module_name: str, module_group_id: int) -> int:
        """
        Create new module

        Args:
            module_name (str): name of module group
            module_group_id (int): id module group to which assign
        
        Raises:
            ModuleNotCreatedError: Invalid data or module group not exists
            ModuleServiceError: Something went wrong, while procesing
        """
        
        try:
            new_module = Modules(
                module_group_id=module_group_id,
                name=module_name,
            )
            module = self.module_repo.add_module_group(new_module)
            
            return module.id
        except ModuleNotAddedError as e:
            raise ModuleNotCreatedError from e
        except CreateExecutionError as e:
            raise ModuleServiceError("Unable to create module")
            
from datetime import datetime

from app.repositories.module import ModuleRepository
from app.models.users import Users
from app.exceptions.domain.module import ModuleNotFoundError
from app.exceptions.infrastucture.repository import QueryExecutionError
from app.exceptions.infrastucture.module import ModuleServiceError
from app.utils import utils

class ModuleService:
    def __init__(
        self, 
        module_repo: ModuleRepository, 
    ):
        self.module_repo = module_repo
        
    def get_user_modules(self, user_id: int) -> dict[str, list[str]]:
        
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
            ModuleNotAssignedError: Invalid data or service module  not exists 
                or module active
            ModuleServiceError: Something went wrong, while procesing
        """
        

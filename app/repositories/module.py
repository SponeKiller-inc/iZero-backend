from datetime import datetime
from typing import Tuple

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .base import BaseRepository
from app.models.user_modules import UserModules
from app.models.modules import Modules
from app.models.module_groups import ModuleGroups
from app.exceptions.repository.module import (
    UserModuleNotAddedError,
    ModuleGroupNotAddedError,
    ModuleNotAddedError,
)
from app.exceptions.infrastucture.repository import QueryExecutionError, CreateExecutionError

class ModuleRepository(BaseRepository):
    
    def get_user_modules(self, user_id: int) -> dict[str, list[str]] | None:
        """
        Retrieve available user modules

        Args:
            user_id (int): user id

        Returns:
            dict[str, list[str]] or None:  modules or None
            
        Raises:
            QueryExecutionError - server side error while execution
        """
        try: 
            rows: list[Tuple[UserModules, Modules, ModuleGroups]] = (
                self.db
                    .query(UserModules, Modules, ModuleGroups)
                    .join(Modules, UserModules.module_id == Modules.id)
                    .join(ModuleGroups, Modules.module_group_id == ModuleGroups.id)
                    .filter(
                        UserModules.user_id == user_id,
                        UserModules.is_current(),
                    )
                    .order_by(Modules.module_group_id.asc())
                    .all()
            )
            
            if rows:
                ## Process data to output type
                data: dict[str, list[str]] = {}
                for _, module, module_group in rows:
                    data.setdefault(module_group.name, []).append(module.name)
            else:
                data = None
            return data
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to retrieve user data") from e
        
    def is_active_user_module(
        self, 
        user_id: int, 
        module_id: int,
        valid_from: datetime,
        valid_to: datetime,
    ) -> bool:
        """
        Finds if user module is active or not
            

        Args:
            user_id (int): user id
            module_id (int): module id

        Returns:
            bool: if active True, inactive False
                (inactive is consider: exists but not valid or not found)
            
        Raises:
            QueryExecutionError - server side error while execution
        """
        filters = []
        
        filters.append(UserModules.user_id == user_id)
        filters.append(UserModules.module_id == module_id)
        
        if valid_from is not None or valid_to is not None:
            if valid_from is not None:
                filters.append(UserModules.valid_from <= valid_from)
            if valid_to is not None:
                filters.append(UserModules.valid_to >= valid_to)
        else:
            filters.append(UserModules.is_current())
        row = (
                self.db
                    .query(UserModules)
                    .filter(*filters)
                    .first()
            )
        
        if row is None:
            # Not Found any currently active module
            return False
        
        return True
    
    def add_user_module(self, new_user_module: UserModules) -> UserModules:
        """
        Add module to user

        Args:
            new_user_module (UserModules): User module data

        Returns:
            UserModules: Created user module
            
        Raises:
            UserModuleNotAddedError - Invalid data or module not exists
            CreateExecutionError - server side error while inserting data
        """
        try:
            self.db.add(new_user_module)
            self.db.commit()
            
            self.db.refresh(new_user_module)
            return new_user_module
        except IntegrityError as e:
            raise UserModuleNotAddedError from e
        except SQLAlchemyError as e:
            raise CreateExecutionError(
                "Unable to add user modules"
            ) from e
            
    def add_module_group(self, new_module_group: ModuleGroups) -> ModuleGroups:
        """
        Add new module group

        Args:
            new_module_group (ModuleGroups): Module group data

        Returns:
            ModuleGroups: Created module group
            
        Raises:
            ModuleGroupNotAddedError - Invalid data - module group name empty
            CreateExecutionError - server side error while inserting data
        """
        
        try:
            self.db.add(new_module_group)
            self.db.commit()
            
            self.db.refresh(new_module_group)
            return new_module_group
        except IntegrityError as e:
            raise ModuleGroupNotAddedError from e
        except SQLAlchemyError as e:
            raise CreateExecutionError(
                "Unable to add module group"
            ) from e
            
    def add_module(self, new_module: Modules) -> Modules:
        """
        Add new module

        Args:
            new_module (Modules): module data

        Returns:
            Modules: created module
            
        Raises:
            ModuleNotAddedError - Invalid data or module group not exists
            CreateExecutionError - server side error while inserting data
        """
        
        try:
            self.db.add(new_module)
            self.db.commit()
            
            self.db.refresh(new_module)
            return new_module
        except IntegrityError as e:
            raise ModuleNotAddedError from e
        except SQLAlchemyError as e:
            raise CreateExecutionError(
                "Unable to add module"
            ) from e
            
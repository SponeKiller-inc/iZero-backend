from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import Tuple

from .base import BaseRepository
from app.models.user_modules import UserModules
from app.models.modules import Modules
from app.models.module_groups import ModuleGroups
from app.exceptions.infrastucture.repository import QueryExecutionError, CreateExecutionError

class ModuleRepository(BaseRepository):
    
    def get_user_modules(self, user_id: str) -> dict[str, list[str]] | None:
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
                        UserModules.is_current())
                    .order_by(Modules.module_group_id.asc())
                    .all()
            )
            
            if rows:
                ## Process data to output type
                data: dict[str, list[str]] = {}
                for _, module, module_group in rows:
                    data = data.setdefault(module_group.name, []).append(module.name)
            else:
                data = None
            return data
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to retrieve user data") from e
    
    def add_user_module(self, new_user_module: UserModules) -> UserModules:
        try:
            self.db.add(new_user_module)
            self.db.commit()
            
            self.db.refresh(new_user_module)
            return new_user_module
        except IntegrityError as e:
            raise UserModuleNotAddedError from e
        except SQLAlchemyError as e:
            raise  CreateExecutionError(
                "Unable to add user modules"
            ) from e
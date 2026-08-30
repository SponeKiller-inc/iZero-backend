from datetime import datetime

from app.domain.modules.entities.module import Module
from app.domain.shared.value_objects.period import ValidityPeriod
from app.infrastructure.repositories.base import BaseAlchemyRepository
from app.infrastructure.models.module.module import ModuleModel

class AlchemyModuleRepository(BaseAlchemyRepository):

    def get(self, module_id: int, ref_date: datetime) -> Module | None:
        """
        Get module by ID
        
        Args:
            module_id: Module ID
            ref_date: Reference date
        
        Returns:
            Module entity if found
        """

        module_model = (
            self.db
                .query(ModuleModel)
                .filter(
                    ModuleModel.id == module_id,
                    ModuleModel.valid_at(ref_date)
                )
                .first()
        )

        if not module_model:
            return None

        return self._to_entity(module_model)

    def save(self, module: Module) -> Module:
        """
        Save module
        
        Args:
            module: Module entity
        
        Returns:
            Module entity
        """

        if module.id is None:
            return self._insert(module)
        else:
            return self._update(module)

    def _insert(self, module: Module) -> Module:
        """
        Insert module
        
        Args:
            module: Module entity
        
        Returns:
            Module entity
        """

        module_model = ModuleModel(
            name=module.name,
            module_group_id=module.module_group_id,
            valid_from=module.validity.valid_from,
            valid_to=module.validity.valid_to,
        )

        self.db.add(module_model)
        self.db.commit()
        self.db.refresh(module_model)

        return self._to_entity(module_model)

    def _update(self, module: Module) -> Module:
        """
        Update module
        
        Args:
            module: Module entity
        
        Returns:
            Module entity
        """

        module_model = (
            self.db
                .query(ModuleModel)
                .filter(ModuleModel.id == module.id)
                .first()
        )

        module_model.name = module.name
        module_model.module_group_id = module.module_group_id
        module_model.valid_from = module.validity.valid_from
        module_model.valid_to = module.validity.valid_to

        self.db.commit()
        self.db.refresh(module_model)

        return self._to_entity(module_model)

    @staticmethod
    def _to_entity(module_model: ModuleModel) -> Module:
        return Module(
            id=module_model.id,
            name=module_model.name,
            module_group_id=module_model.module_group_id,
            validity=ValidityPeriod(
                valid_from=module_model.valid_from,
                valid_to=module_model.valid_to,
            ),
        )
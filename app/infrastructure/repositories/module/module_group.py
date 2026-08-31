from datetime import datetime
from app.domain.modules.entities.module_group import ModuleGroup
from app.domain.shared.value_objects.period import ValidityPeriod
from app.infrastructure.repositories.base import BaseAlchemyRepository
from app.infrastructure.models.module.module_group import ModuleGroupModel

class AlchemyModuleGroupRepository(BaseAlchemyRepository):
    def get(self, module_group_id: int, ref_date: datetime) -> ModuleGroup | None:
        """
        Get module group by id
        
        Args:
            module_group_id: Module group id
            ref_date: Reference date
        
        Returns:
            Module group if found
        """

        module_group_model = (
            self.db
                .query(ModuleGroupModel)
                .filter(ModuleGroupModel.id == module_group_id)
                .first()
        )

        if not module_group_model:
            return None

        return self._to_entity(module_group_model)

    def save(self, module_group: ModuleGroup) -> ModuleGroup:
        """
        Save module group
        
        Args:
            module_group: Module group entity
        
        Returns:
            Module group entity
        """

        if module_group.id is None:
            return self._insert(module_group)
        else:
            return self._update(module_group)

    def _insert(self, module_group: ModuleGroup) -> ModuleGroup:
        """
        Insert module group
        
        Args:
            module_group: Module group entity
        
        Returns:
            Module group entity
        """
        module_group_model = ModuleGroupModel(
            name=module_group.name,
            valid_from=module_group.validity.valid_from,
            valid_to=module_group.validity.valid_to,
        )
        self.db.add(module_group_model)
        self.db.commit()
        self.db.refresh(module_group_model)

        return self._to_entity(module_group_model)
    
    def _update(self, module_group: ModuleGroup) -> ModuleGroup:
        """
        Update module group
        
        Args:
            module_group: Module group entity
        
        Returns:
            Module group entity
        """
        module_group_model = (
            self.db
                .query(ModuleGroupModel)
                .filter(ModuleGroupModel.id == module_group.id)
                .first()
        )

        module_group_model.name = module_group.name
        module_group_model.valid_from = module_group.validity.valid_from
        module_group_model.valid_to = module_group.validity.valid_to

        self.db.add(module_group_model)
        self.db.commit()
        self.db.refresh(module_group_model)

        return self._to_entity(module_group_model)

    @staticmethod
    def _to_entity(module_group_model: ModuleGroupModel) -> ModuleGroup:
        return ModuleGroup(
            id=module_group_model.id,
            name=module_group_model.name,
            validity=ValidityPeriod(
                valid_from=module_group_model.valid_from,
                valid_to=module_group_model.valid_to,
            ),
        )
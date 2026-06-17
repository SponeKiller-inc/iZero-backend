from typing import Protocol, Optional

from app.domain.modules.entities.module_group import ModuleGroup

class ModuleGroupRepository(Protocol):
    def get(self, module_group_id: int) -> Optional[ModuleGroup]:
        """
        Get module group by id

        Args:
            module_group_id: Module group id
        
        Returns:
            Module group if found
        """
        ...

    def save(self, module_group: ModuleGroup) -> ModuleGroup:
        """
        Save new or existing module group

        Args:
            module_group: Module group to save

        Returns:
            Updated or new module group
        """
        ...
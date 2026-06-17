from typing import Protocol, Optional

from app.domain.modules.entities.module import Module

class ModuleRepository(Protocol):
    def get(self, module_id: int) -> Optional[Module]:
        """
        Get module by id

        Args:
            module_id: Module id
        
        Returns:
            Module if found
        """
        ...

    def get_user_modules(self, user_id: int) -> list[Module]:
        """
        Get user modules

        Args:
            user_id: User id

        Returns:
            List of modules
        """
        ...

    def save(self, module: Module) -> Module:
        """
        Save new or existing module

        Args:
            module: Module to save

        Returns:
            Updated or new module
        """
        ...
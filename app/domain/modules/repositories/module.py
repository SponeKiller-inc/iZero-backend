from datetime import datetime
from typing import Protocol

from app.domain.modules.entities.module import Module

class ModuleRepository(Protocol):
    def get(self, module_id: int, ref_date: datetime) -> Module | None:
        """
        Get module by id

        Args:
            module_id: Module id
            ref_date: Reference date
        
        Returns:
            Module if found
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
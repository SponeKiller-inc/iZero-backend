from app.domain.modules.entities.module import Module
from app.domain.shared.value_objects.period import ValidityPeriod

class ModuleGroup:
    def __init__(
        self, 
        id: int, 
        name: str, 
        validity: ValidityPeriod,
        modules: list[Module] | None = None
    ):
        self.id = id
        self.name = name
        self.validity = validity
        self.modules = modules or []

    def create_module(
        self, 
        module_id: int, 
        name: str, 
        module_group_id: int
    ) -> Module:
        """
        Add new module to module group

        Args:
            module_id (int): module id which is added
            name (str): name of module which is added
            module_group_id (int): id module group to which assign
        
        Returns:
            Module: new module which is added
        """
        new_module = Module(module_id, name, module_group_id)
        self.modules.append(new_module)
        return new_module
from pydantic import BaseModel


class ModuleSchema(BaseModel):
    """Schema carrying user data to assign module."""
    
    id: int
    name: str


class RetrieveModulesOut(BaseModel):
    """Schema carrying user data to assign module."""

    module_group_id: int
    module_group_name: str
    modules: list[ModuleSchema]
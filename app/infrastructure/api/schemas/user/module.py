from pydantic import BaseModel, ConfigDict


class ModuleSchema(BaseModel):
    """Schema carrying user data to assign module."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RetrieveModulesSchemaOut(BaseModel):
    """Schema carrying user data to assign module."""

    model_config = ConfigDict(from_attributes=True)

    module_group_id: int
    module_group_name: str
    modules: list[ModuleSchema]
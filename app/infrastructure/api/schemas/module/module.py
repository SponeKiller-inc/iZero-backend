from datetime import datetime

from pydantic import BaseModel


class ModuleIn(BaseModel):
    """Schema carrying data to create a module."""

    name: str
    module_group_id: int
    valid_from: datetime


class ModuleOut(BaseModel):
    """Schema carrying created module data."""

    id: int
    name: str
    module_group_id: int
    valid_from: datetime
    valid_to: datetime

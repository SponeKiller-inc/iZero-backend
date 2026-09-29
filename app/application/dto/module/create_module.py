from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateModuleIn:
    """DTO carrying data to create a module."""
    name: str
    module_group_id: int
    valid_from: datetime


@dataclass(frozen=True)
class CreateModuleOut:
    """DTO carrying created module data."""
    id: int
    name: str
    module_group_id: int
    valid_from: datetime
    valid_to: datetime | None

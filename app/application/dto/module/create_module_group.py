from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateModuleGroupIn:
    """DTO carrying data to create a module group."""
    name: str
    valid_from: datetime


@dataclass(frozen=True)
class CreateModuleGroupOut:
    """DTO carrying created module group data."""
    id: int
    name: str
    valid_from: datetime
    valid_to: datetime | None

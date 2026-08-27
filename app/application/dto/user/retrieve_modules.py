from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class RetrieveModulesOut:
    """DTO carrying user data to assign module."""
    module_group_id: int
    module_group_name: str
    modules: list[ModuleDto]

@dataclass(frozen=True)
class ModuleDto:
    """DTO carrying user data to assign module."""
    id: int
    name: str

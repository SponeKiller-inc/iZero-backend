from dataclasses import dataclass


@dataclass(frozen=True)
class AssignModuleIn:
    """DTO carrying user data to assign module."""
    user_id: int
    module_id: int
    duration_days: int

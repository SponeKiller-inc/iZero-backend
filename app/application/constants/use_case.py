from enum import Enum
from typing import Self


class UseCase(str, Enum):
    USER_ASSIGN_MODULE = "assign_module"
    USER_RETRIEVE_MODULE = "retrieve_module"
    AUTH_ASSIGN_ROLE_PERMISSION = "assign_role_permission"

    @classmethod
    def has_member(cls, name: str) -> bool:
        return name in cls.__members__

    @classmethod
    def get_member(cls, name: str) -> Self | None:
        return cls.__members__.get(name)
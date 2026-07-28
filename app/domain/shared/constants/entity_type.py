from enum import StrEnum
from typing import Self

class EntityType(StrEnum):
    ADDRESSES = "addresses"
    USERS = "users"
    AUTH = "auth"
    BANK = "banks"
    SESSION = "session"
    CUSTOMERS = "customers"
    MODULES = "modules"

    @classmethod
    def has_member(cls, name: str) -> bool:
        return name in cls.__members__

    @classmethod
    def get_member(cls, name: str) -> Self | None:
        return cls.__members__.get(name)
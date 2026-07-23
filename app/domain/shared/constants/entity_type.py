from enum import StrEnum

class EntityType(StrEnum):
    ADDRESSES = "addresses"
    USERS = "users"
    AUTH = "auth"
    BANK = "banks"
    SESSION = "session"
    CUSTOMERS = "customers"
    MODULES = "modules"
from enum import StrEnum

class RoleType(StrEnum):
    REGULAR = "regular"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
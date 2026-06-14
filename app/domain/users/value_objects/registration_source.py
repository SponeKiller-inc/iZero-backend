from dataclasses import dataclass

from app.domain.users.constants.registration_source_type import RegistrationSourceType

@dataclass(frozen=True)
class RegistrationSource:
    """
    Value Object representing user role.
    """
    value: RegistrationSourceType
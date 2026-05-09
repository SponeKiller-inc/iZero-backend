from dataclasses import dataclass
from typing import ClassVar
from app.domain.value_objects.base import BaseValueObject

@dataclass(frozen=True)
class RegistrationNumber(BaseValueObject):
    length: ClassVar[int] = 8
    pattern: ClassVar[str] = r"^[A-Z0-9]+$"

@dataclass(frozen=True)
class BusinessTaxNumber(BaseValueObject):
    length: ClassVar[int] = 10
    pattern: ClassVar[str] = r"^[A-Z0-9]+$"

@dataclass(frozen=True)
class ProprietorTaxNumber(BaseValueObject):
    length: ClassVar[int] = 12
    pattern: ClassVar[str] = r"^[A-Z0-9]+$"
from dataclasses import dataclass
from typing import ClassVar
from app.domain.value_objects.base import BaseValueObject

@dataclass(frozen=True)
class BankCode(BaseValueObject):
    length: ClassVar[int] = 4
    pattern: ClassVar[str] = r"^\d{4}$"

@dataclass(frozen=True)
class AccountPrefix(BaseValueObject):
    length: ClassVar[int] = 6
    pattern: ClassVar[str] = r"^\d{1,6}$"

@dataclass(frozen=True)
class AccountNumber(BaseValueObject):
    length: ClassVar[int] = 10
    pattern: ClassVar[str] = r"^\d{1,10}$"

@dataclass(frozen=True)
class Swift(BaseValueObject):
    length: ClassVar[int] = 11
    pattern: ClassVar[str] = r"^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$"

@dataclass(frozen=True)
class Iban(BaseValueObject):
    length: ClassVar[int] = 34
    pattern: ClassVar[str] = r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$"
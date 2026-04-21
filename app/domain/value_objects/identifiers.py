import re
from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Identifier:
    value: str
    length: ClassVar[int] = 0

    def __post_init__(self):
        if not re.match(rf"^[A-Z0-9]{{{self.length}}}$", self.value):
            raise ValueError(
                f"Invalid format for {self.__class__.__name__}. "
                f"Expected length {self.length}, got '{self.value}'"
            )

@dataclass(frozen=True)
class RegistrationNumber(Identifier):
    length: ClassVar[int] = 8

@dataclass(frozen=True)
class BusinessTaxNumber(Identifier):
    length: ClassVar[int] = 10

@dataclass(frozen=True)
class ProprietorTaxNumber(Identifier):
    length: ClassVar[int] = 12
from dataclasses import dataclass
from typing import ClassVar
from app.domain.shared.value_objects.base import BaseValueObject

@dataclass(frozen=True)
class CountryIsoCode(BaseValueObject):
    length: ClassVar[int] = 3
    pattern: ClassVar[str] = r"^[A-Z]{3}$"
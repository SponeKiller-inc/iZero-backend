import re
from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class BaseValueObject:
    value: str
    length: ClassVar[int]
    pattern: ClassVar[str]

    def __post_init__(self):
        if not re.match(self.pattern, self.value):
            raise ValueError(f"Invalid format for {self.__class__.__name__}: {self.value}")
        
        if len(self.value) > self.length:
            raise ValueError(f"{self.__class__.__name__} is too long (max {self.length})")
from typing import Type, Any, get_type_hints
from sqlalchemy import String, Integer
from sqlalchemy.types import TypeDecorator

class ValueObjectType(TypeDecorator):
    cache_ok = True

    def __init__(self, cls: Type[Any], *args: Any, **kwargs: Any):
        self.cls = cls
        
        # 1. Get type
        hints = get_type_hints(cls)
        if "value" not in hints:
            raise TypeError(
                f"Value Object {cls.__name__} must have a 'value' type hint."
            )
        
        inner_type = hints["value"]
        
        # 2. Get length
        length = getattr(cls, 'length', None)

        # 3. Auto-assign implementation
        if issubclass(inner_type, int):
            self.impl = Integer
        elif issubclass(inner_type, str):
            self.impl = String(length) if length is not None else String
        else:
            # possible extension for other types (e.g. float -> Float)
            raise NotImplementedError(
                f"Mapping for type {inner_type} is not implemented."
            )
            
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        return value.value if value is not None else None

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        return self.cls(value) if value is not None else None
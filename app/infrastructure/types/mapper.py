from typing import Type, Any, Optional
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.types import TypeDecorator, TypeEngine, String

class ValueObjectType(TypeDecorator):
    cache_ok = True

    def __init__(
        self, 
        cls: Type[Any], 
        storage_type: Type[TypeEngine] | TypeEngine = String, 
        *args: Any, 
        **kwargs: Any
    ):
        self.cls = cls
        self.impl = storage_type
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[Any]:
        return value.value if value is not None else None

    def process_result_value(self, value: Any, dialect: Dialect) -> Optional[Any]:
        return self.cls(value) if value is not None else None
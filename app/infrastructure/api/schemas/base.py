from typing import Any, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse as _JSONResponse
from pydantic import BaseModel

from app.infrastructure.api.schemas.message_id import MessageId


class ResponseContainer[T](BaseModel):
    message_id: Optional[MessageId] = None
    message: Optional[str] = None
    data: Optional[T] = None


class JSONResponse(_JSONResponse):
    """JSONResponse that encodes its content (e.g. ResponseContainer) automatically."""

    def render(self, content: Any) -> bytes:
        return super().render(jsonable_encoder(content))

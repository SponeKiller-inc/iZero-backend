from typing import Optional
from pydantic import BaseModel


class ResponseContainer[T](BaseModel):
    message_id: Optional[str] = None
    message: Optional[str] = None
    data: Optional[T] = None
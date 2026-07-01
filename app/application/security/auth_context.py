from contextvars import ContextVar
from typing import Optional

class AuthContext:
    def __init__(self):
        self._id_ctx: ContextVar[Optional[int]] = ContextVar("current_user_id", default=None)

    def set(self, user_id: int) -> None:
        self._id_ctx.set(user_id)

    def get(self) -> int:
        user_id = self._id_ctx.get()
        if user_id is None:
            return 0
        return user_id

    def clear(self) -> None:
        self._id_ctx.set(None)
from contextvars import ContextVar

class AuthContext:
    _id_ctx: ContextVar[int | None] = ContextVar(
        "current_user_id",
        default=None
    )

    @classmethod
    def set(cls, user_id: int) -> None:
        """
        Set auth context for current request
        
        Args:
            user_id: user id for request
        """
        cls._id_ctx.set(user_id)

    @classmethod
    def get(cls) -> int | None:
        """
        Get user id from auth context

        Returns:
            user_id or None if not set
        """
        return cls._id_ctx.get()  

    @classmethod
    def clear(cls) -> None:
        """
        Clear auth context
        """
        cls._id_ctx.set(None)
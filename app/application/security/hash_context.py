from contextvars import ContextVar

class HashContext:
    _hash_ctx: ContextVar[str | None] = ContextVar(
        "hash",
        default=None
    )

    @classmethod
    def set(cls, hash_val: str) -> None:
        """
        Set hash context for current request
        
        Args:
            hash_val: hash for request
        """
        cls._hash_ctx.set(hash_val)

    @classmethod
    def get(cls) -> str | None:
        """
        Get hash from hash context

        Returns:
            hash or None if not set
        """
        return cls._hash_ctx.get()  

    @classmethod
    def clear(cls) -> None:
        """
        Clear hash context
        """
        cls._hash_ctx.set(None)
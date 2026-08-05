from contextvars import ContextVar

class HashContext:
    _hash_ctx: ContextVar[list[str]] = ContextVar(
        "hash",
        default=[]
    )

    @classmethod
    def set(cls, hash_val: list[str]) -> None:
        """
        Set hash context for current request
        
        Args:
            hash_val: hash for request
        """
        cls._hash_ctx.set(hash_val)

    @classmethod
    def get(cls) -> list[str]:
        """
        Get hash from hash context

        Returns:
            hash or empty list if not set
        """
        return cls._hash_ctx.get()  

    @classmethod
    def clear(cls) -> None:
        """
        Clear hash context
        """
        cls._hash_ctx.set([])
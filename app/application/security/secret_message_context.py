import secrets
from contextvars import ContextVar


class SecretMessageContext:
    _msg_ctx: ContextVar[str] = ContextVar(
        f"SECRET_MESSAGE_{secrets.token_hex(16)}",
        default=secrets.token_hex(16)
    )

    @classmethod
    def get(cls) -> str:
        """
        Get secret message from auth context

        Returns:
            secret message
        """
        return cls._msg_ctx.get()
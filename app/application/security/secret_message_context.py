import secrets
from contextvars import ContextVar


class SecretMessageContext:
    _msg_ctx: ContextVar[str] = ContextVar(
        f"SECRET_MESSAGE_{secrets.token_hex(16)}"
    )

    @classmethod
    def get(cls) -> str:
        """
        Get secret message from auth context

        Returns:
            secret message
        """
        value = cls._msg_ctx.get(None)
        if value is None:
            value = secrets.token_hex(16)
            cls._msg_ctx.set(value)
        return value
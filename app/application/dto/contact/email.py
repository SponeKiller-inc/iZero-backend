from dataclasses import dataclass


@dataclass(frozen=True)
class EmailOut:
    """DTO carrying an e-mail."""
    id: int
    address: str

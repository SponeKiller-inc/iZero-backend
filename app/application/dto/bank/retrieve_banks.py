from dataclasses import dataclass


@dataclass(frozen=True)
class RetrieveBankOut:
    """DTO carrying bank data of the bank catalogue."""
    id: int
    name: str
    address_id: int
    code: str
    swift: str

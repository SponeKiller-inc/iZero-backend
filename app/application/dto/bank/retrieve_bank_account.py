from dataclasses import dataclass

from app.application.dto.bank.retrieve_banks import RetrieveBankOut


@dataclass(frozen=True)
class RetrieveBankAccountOut:
    """DTO carrying bank account data together with its bank."""
    id: int
    owner_name: str
    account_prefix: str
    account_number: str
    iban: str
    bank: RetrieveBankOut

from pydantic import BaseModel, ConfigDict

from app.infrastructure.api.schemas.bank.bank_account import BankSchemaOut


class UserBankAccountSchemaIn(BaseModel):
    """Schema carrying bank account data to add or change."""

    bank_id: int
    owner_name: str
    # Accounts without prefix are stored with zeros
    account_prefix: str = "000000"
    account_number: str
    iban: str


class UserBankAccountSchemaOut(BaseModel):
    """Schema carrying the user's bank account together with its bank."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_name: str
    account_prefix: str
    account_number: str
    iban: str
    bank: BankSchemaOut

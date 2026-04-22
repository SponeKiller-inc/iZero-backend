from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.types.bank_identification import (
    AccountPrefix,
    AccountNumber,
    Iban,
)

class BankAccountModel(Base):
    __tablename__ = "bank_accounts"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    owner_name: Mapped[str] = mapped_column()
    account_prefix: Mapped[AccountPrefix] = mapped_column()
    account_number: Mapped[AccountNumber] = mapped_column()
    iban: Mapped[Iban] = mapped_column()
    
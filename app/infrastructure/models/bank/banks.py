from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.types.identification import (
    RegistrationNumber,
    BusinessTaxNumber,
)
from app.infrastructure.types.bank_identification import (
    BankCode,
    Swift,
)


class BankModel(Base):
    __tablename__ = "banks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[RegistrationNumber] = mapped_column()
    tax_number: Mapped[BusinessTaxNumber] = mapped_column()
    code: Mapped[BankCode] = mapped_column(unique=True)
    swift_code: Mapped[Swift] = mapped_column(unique=True)
    
    
    
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, ValidityMixin

class BankAddresses(Base, ValidityMixin):
    __tablename__ = "bank_addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    
    
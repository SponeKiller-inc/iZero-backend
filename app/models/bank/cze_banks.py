from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.types.cze_identifiers import (
    registration_number,
    business_tax_number,
)

class CzeBanks(Base):
    __tablename__ = "cze_banks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[registration_number] = mapped_column()
    tax_number: Mapped[business_tax_number] = mapped_column()
    
    
    
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class CzeBanks(Base):
    __tablename__ = "cze_banks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    owner_name: Mapped[str] = mapped_column()
    prefix: Mapped[str] = mapped_column(String(6))
    account_number: Mapped[str] = mapped_column(String(10))
    iban: Mapped[str] = mapped_column(String(24))
    
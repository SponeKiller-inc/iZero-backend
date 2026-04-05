from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class CzechAddresses(Base):
    __tablename__ = "czech_addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ruian_id: Mapped[int] = mapped_column(unique=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    street: Mapped[str | None] = mapped_column(String(48))
    number_type: Mapped[str] = mapped_column(String(4))
    building_number: Mapped[int] = mapped_column()
    orientation_number: Mapped[int | None] = mapped_column()
    orientation_number_letter: Mapped[str | None] = mapped_column(String(1))
    district: Mapped[str | None] = mapped_column(String(48))
    city: Mapped[str] = mapped_column(String(48))
    postal_code: Mapped[str] = mapped_column(String(5))
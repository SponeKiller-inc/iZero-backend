from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class CzeAddresses(Base):
    __tablename__ = "cze_addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    street_name: Mapped[str] = mapped_column()
    house_number: Mapped[str] = mapped_column()
    district: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    postal_code: Mapped[str] = mapped_column()
    region: Mapped[str] = mapped_column()
    
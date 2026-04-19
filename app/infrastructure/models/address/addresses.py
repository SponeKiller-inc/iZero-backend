from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class AddressModel(Base):
    __tablename__ = "addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ruian_id: Mapped[int] = mapped_column(unique=True)
    street: Mapped[str | None] = mapped_column(String(48))
    number_type: Mapped[str] = mapped_column(String(4))
    building_number: Mapped[int] = mapped_column()
    orientation_number: Mapped[int | None] = mapped_column()
    orientation_number_letter: Mapped[str | None] = mapped_column(String(1))
    district: Mapped[str | None] = mapped_column(String(48))
    city: Mapped[str] = mapped_column(String(48))
    postal_code: Mapped[str] = mapped_column(String(5))

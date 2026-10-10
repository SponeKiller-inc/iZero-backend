from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class AddressModel(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[int] = mapped_column()
    street: Mapped[str | None] = mapped_column(String(48))
    building_number: Mapped[str] = mapped_column(String(10))
    orientation_number: Mapped[str | None] = mapped_column(String(10))
    orientation_number_letter: Mapped[str | None] = mapped_column(String(1))
    district: Mapped[str | None] = mapped_column(String(48))
    city: Mapped[str] = mapped_column(String(48))
    postal_code: Mapped[int] = mapped_column()
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    __table_args__ = (
        UniqueConstraint(
            "external_id", "country_id",
            name="uq_addresses_external_id_country_id",
        ),
    )
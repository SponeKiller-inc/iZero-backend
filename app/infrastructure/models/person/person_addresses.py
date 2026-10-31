from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, ValidityMixin


class PersonAddressModel(Base, ValidityMixin):
    __tablename__ = "person_addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address_type_id: Mapped[int] = mapped_column(ForeignKey("address_types.id"))

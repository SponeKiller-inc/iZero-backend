from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, ValidityMixin

class UserAddressModel(Base, ValidityMixin):
    __tablename__ = "user_addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address_type_id: Mapped[int] = mapped_column(ForeignKey("address_types.id"))
    
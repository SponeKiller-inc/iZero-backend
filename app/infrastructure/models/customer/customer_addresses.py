from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, ValidityMixin

class CustomerAddressModel(Base, ValidityMixin):
    __tablename__ = "customer_addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    address_type_id: Mapped[int] = mapped_column(ForeignKey("address_types.id"))
    
    
    
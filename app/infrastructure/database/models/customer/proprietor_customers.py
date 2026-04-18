from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.types.identifiers import (
    registration_number,
    proprietor_tax_number,
)

class ProprietorCustomers(Base):
    __tablename__ = "proprietor_customers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        unique=True,
    )
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[registration_number] = mapped_column()
    tax_number: Mapped[proprietor_tax_number] = mapped_column()
    is_vat_payer: Mapped[bool] = mapped_column(default=False)
    phone_id: Mapped[int] = mapped_column(ForeignKey("phones.id"))
    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"))
    
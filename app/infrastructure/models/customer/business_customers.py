from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.types.identification import (
    RegistrationNumber,
    BusinessTaxNumber,
)

class BusinessCustomerModel(Base):
    __tablename__ = "business_customers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        unique=True,
    )
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[RegistrationNumber] = mapped_column()
    tax_number: Mapped[BusinessTaxNumber] = mapped_column()
    is_vat_payer: Mapped[bool] = mapped_column(default=False)
    phone_id: Mapped[int] = mapped_column(ForeignKey("phones.id"))
    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"))
    
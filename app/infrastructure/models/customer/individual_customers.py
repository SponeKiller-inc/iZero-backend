from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class IndividualCustomerModel(Base):
    __tablename__ = "individual_customers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        unique=True,
    )
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id", ondelete="CASCADE"))
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    phone_id: Mapped[int] = mapped_column(ForeignKey("phones.id"))
    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"))
    
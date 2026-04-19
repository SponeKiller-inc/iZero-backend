from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.database.models.types.identifiers import business_tax_number, registration_number


class BankModel(Base):
    __tablename__ = "banks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[registration_number] = mapped_column()
    tax_number: Mapped[business_tax_number] = mapped_column()
    code: Mapped[str] = mapped_column(String(4), unique=True)
    swift_code: Mapped[str] = mapped_column(String(11), unique=True)
    
    
    
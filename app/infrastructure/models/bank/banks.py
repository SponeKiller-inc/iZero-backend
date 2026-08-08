from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from sqlalchemy import String


class BankModel(Base):
    __tablename__ = "banks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[str] = mapped_column(String(50))
    tax_number: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(String(10), unique=True)
    swift_code: Mapped[str] = mapped_column(String(20), unique=True)
    
    
    
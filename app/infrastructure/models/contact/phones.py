from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class PhoneModel(Base):
    __tablename__ = "phones"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(unique=True)
    
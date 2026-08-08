from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class EmailModel(Base):
    __tablename__ = "emails"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(unique=True)

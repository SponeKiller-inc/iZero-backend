from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from sqlalchemy import String

class CountryModel(Base):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    name: Mapped[str] = mapped_column()
    
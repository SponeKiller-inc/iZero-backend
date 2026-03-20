from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class CountryCodes(Base):
    __tablename__ = "country_codes"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    description: Mapped[str] = mapped_column()
    
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Banks(Base):
    __tablename__ = "banks"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_code_id: Mapped[int] = mapped_column(ForeignKey("country_codes.id"))

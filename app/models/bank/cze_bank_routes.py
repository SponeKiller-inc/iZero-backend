from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class CzeBanksRoutes(Base):
    __tablename__ = "cze_bank_routes"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    code: Mapped[str] = mapped_column(String(4), unique=True)
    swift_code: Mapped[str] = mapped_column(String(11), unique=True)
    
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class PhonePrefixModel(Base):
    __tablename__ = "phone_prefixes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prefix: Mapped[str] = mapped_column(String(3), unique=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

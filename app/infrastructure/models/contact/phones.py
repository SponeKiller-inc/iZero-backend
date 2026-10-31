from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class PhoneModel(Base):
    __tablename__ = "phones"
    __table_args__ = (
        UniqueConstraint("phone_prefix_id", "number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone_prefix_id: Mapped[int] = mapped_column(ForeignKey("phone_prefixes.id"))
    number: Mapped[str] = mapped_column(String(9))

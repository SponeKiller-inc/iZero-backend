from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class InternalRequestLogModel(Base):
    __tablename__ = "internal_request_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method: Mapped[str] = mapped_column(String(10))
    url: Mapped[str] = mapped_column(Text)
    headers: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)

from sqlalchemy import Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class InternalResponseLogModel(Base):
    __tablename__ = "internal_response_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("internal_request_log.id", ondelete="CASCADE"),
    )
    status_code: Mapped[int | None] = mapped_column()
    headers: Mapped[str | None] = mapped_column(Text)
    body: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[float] = mapped_column(Float)
    error: Mapped[str | None] = mapped_column(Text)

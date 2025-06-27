from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey, 
    JSON,
)

from app.database.base import Base

class Sessions(Base):
    __tablename__ = "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    event_type: Mapped[str] = mapped_column(nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)

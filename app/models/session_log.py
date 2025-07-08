from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
)

from app.database.base import Base

class SessionLog(Base):
    __tablename__ = "session_log"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    event_type: Mapped[str] = mapped_column(nullable=False)

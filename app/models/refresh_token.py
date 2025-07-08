from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import (
    ForeignKey, 
    DateTime,
    CheckConstraint,
    func,
)

from app.database.base import Base
class RefreshToken(Base):
    __tablename__ = "refresh_token"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    token: Mapped[str] = mapped_column(nullable=False)
    expired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    
    __table_args__ = (
        CheckConstraint(
            expired_at > func.now(),
            name="ck_expired_at_in_future"
        ),
    )
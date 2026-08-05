from app.infrastructure.database.base import ValidityMixin
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import (
    ForeignKey, 
    DateTime,
    CheckConstraint,
    func,
)

from app.infrastructure.database.base import Base

class RefreshTokenModel(Base, ValidityMixin):
    __tablename__ = "refresh_token"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[string] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False
    )
    token: Mapped[str] = mapped_column(nullable=False)

    
    __table_args__ = (
        CheckConstraint(
            expired_at > func.now(),
            name="ck_expired_at_in_future"
        ),
    )
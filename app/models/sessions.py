from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey, 
    JSON,
)

from app.database.base import Base

class Sessions(Base):
    __tablename__ = "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=True
    )
    ip_address: Mapped[str] = mapped_column(nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)

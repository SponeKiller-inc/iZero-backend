from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, ValidityMixin


class RefreshTokenModel(Base, ValidityMixin):
    __tablename__ = "refresh_token"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), 
        nullable=False,
        index=True,
    )
    token: Mapped[str] = mapped_column(nullable=False)

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, CheckConstraint

from app.database.base import Base

class UserModules(Base):
    __tablename__ = "user_modules"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,        
    )
    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
    )
    valid_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    valid_to: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    
    __table_args__ = (
        CheckConstraint(
            valid_to > valid_from,
            name="ck_valid_to_greater_than_valid_from"
        ),
    )
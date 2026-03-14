from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database.base import Base

class UserRoles(Base):
    __tablename__ = "user_roles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    role_type_id: Mapped[int] = mapped_column(
        ForeignKey("role_types.id", ondelete="CASCADE"),
        nullable=False,
    )
    
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.infrastructure.database.base import Base, ValidityMixin

class UserRoleModel(Base, ValidityMixin):
    __tablename__ = "user_roles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role_type_id: Mapped[int] = mapped_column(ForeignKey("role_types.id", ondelete="CASCADE"))
    
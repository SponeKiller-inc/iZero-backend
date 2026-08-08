from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import ValidityMixin
from app.infrastructure.database.base import Base

class RolePermissionModel(Base, ValidityMixin):
    __tablename__ = "role_permission"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    entity_type: Mapped[str] = mapped_column()
    method: Mapped[str] = mapped_column()
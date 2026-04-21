from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class RoleTypeModel(Base):
    __tablename__ = "role_types"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    
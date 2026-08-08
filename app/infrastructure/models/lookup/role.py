from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class RoleModel(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    disabled: Mapped[bool] = mapped_column()
    
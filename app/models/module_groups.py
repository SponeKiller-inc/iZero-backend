from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class ModuleGroups(Base):
    __tablename__ = "modules_groups"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
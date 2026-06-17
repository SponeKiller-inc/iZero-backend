from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, ValidityMixin

class ModuleGroupModel(Base, ValidityMixin):
    __tablename__ = "module_groups"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
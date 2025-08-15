from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database.base import Base

class Modules(Base):
    __tablename__ = "modules"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    module_group_id: Mapped[int] = mapped_column(
        ForeignKey("module_groups.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    
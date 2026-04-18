from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class EntityTypes(Base):
    __tablename__ = "entity_types"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    
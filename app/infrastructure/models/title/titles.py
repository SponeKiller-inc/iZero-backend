from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.infrastructure.database.base import Base, ValidityMixin

class TitleType(enum.Enum):
    prefix = "prefix"
    suffix = "suffix"

class TitleModel(Base, ValidityMixin):
    __tablename__ = "titles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_type: Mapped[TitleType] = mapped_column()

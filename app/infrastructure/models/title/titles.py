from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class TitleModel(Base):
    __tablename__ = "titles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_type: Mapped[str] = mapped_column()

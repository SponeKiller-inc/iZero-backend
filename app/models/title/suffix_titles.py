from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.database.base import Base, ValidityMixin

class SuffixTitles(Base, ValidityMixin):
    __tablename__ = "suffix_titles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column()
    priority: Mapped[int] = mapped_column()

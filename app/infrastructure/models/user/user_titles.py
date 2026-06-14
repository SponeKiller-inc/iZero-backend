from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.infrastructure.database.base import Base, ValidityMixin

class UserTitleModel(Base, ValidityMixin):
    __tablename__ = "user_titles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id", ondelete="CASCADE"))

    
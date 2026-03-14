from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, ValidityMixin

class Customers(Base, ValidityMixin):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_type_id: Mapped[int] = mapped_column(
        ForeignKey("entity_types.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
    )
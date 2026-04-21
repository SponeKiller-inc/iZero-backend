from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class CustomerModel(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_type_id: Mapped[int] = mapped_column(
        ForeignKey("entity_types.id", ondelete="CASCADE"),
        nullable=False,
    )
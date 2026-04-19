from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class AddressTypeModel(Base):
    __tablename__ = "address_types"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column()
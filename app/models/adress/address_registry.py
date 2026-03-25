from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class AddressRegistry(Base):
    __tablename__ = "address_registry"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_name: Mapped[str] = mapped_column()
    country_code_id: Mapped[int] = mapped_column(ForeignKey("country_codes.id"))
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, ValidityMixin

class AddressRegistry(Base, ValidityMixin):
    __tablename__ = "address_registry"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_name: Mapped[str] = mapped_column()
    country_code_id: Mapped[int] = mapped_column(ForeignKey("country_codes.id"))
    
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from app.infrastructure.types.location import CountryIsoCode

class CountryModel(Base):
    __tablename__ = "countries"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[CountryIsoCode] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    
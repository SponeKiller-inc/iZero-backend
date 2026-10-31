from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class NaturalPersonModel(Base):
    __tablename__ = "natural_persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        unique=True,
    )
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    date_of_birth: Mapped[date] = mapped_column(Date)
    phone_id: Mapped[int | None] = mapped_column(ForeignKey("phones.id"))
    email_id: Mapped[int | None] = mapped_column(ForeignKey("emails.id"))

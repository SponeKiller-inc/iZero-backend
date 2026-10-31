from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class EntrepreneurModel(Base):
    __tablename__ = "entrepreneurs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        unique=True,
    )
    name: Mapped[str] = mapped_column()
    registration_number: Mapped[str] = mapped_column(String(8))
    vat_number: Mapped[str | None] = mapped_column(String(12))
    is_vat_payer: Mapped[bool] = mapped_column(default=False)
    phone_id: Mapped[int | None] = mapped_column(ForeignKey("phones.id"))
    email_id: Mapped[int | None] = mapped_column(ForeignKey("emails.id"))

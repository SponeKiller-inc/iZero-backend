from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class CompanyModel(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        unique=True,
    )
    name: Mapped[str] = mapped_column()
    legal_form_id: Mapped[int] = mapped_column(ForeignKey("legal_forms.id"))
    registration_number: Mapped[str] = mapped_column(String(8), unique=True)
    vat_number: Mapped[str | None] = mapped_column(String(12))
    is_vat_payer: Mapped[bool] = mapped_column(default=False)
    representative_person_id: Mapped[int] = mapped_column(
        ForeignKey("natural_persons.person_id"),
        index=True,
    )
    phone_id: Mapped[int | None] = mapped_column(ForeignKey("phones.id"))
    email_id: Mapped[int | None] = mapped_column(ForeignKey("emails.id"))

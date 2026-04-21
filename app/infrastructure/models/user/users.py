from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    CheckConstraint,
    or_,
    event,
)

from app.infrastructure.database.base import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(nullable=False, default="local")
    provider_user_id: Mapped[str | None] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str | None] = mapped_column(nullable=True)
    
    __table_args__ = (
        CheckConstraint(
                or_(provider == 'local', provider_user_id.isnot(None)),
                name='chk_need_fill_provider_user_id'
        ),
        CheckConstraint(
            or_(provider != 'local', password.isnot(None)),
            name="chk_need_fill_password"
        ),
    )

@event.listens_for(UserModel, "before_insert", propagate=True)
@event.listens_for(UserModel, "before_update", propagate=True)
def _lowercase_email(mapper, connection, target: UserModel) -> None:
    if target.email:
        target.email = target.email.lower()

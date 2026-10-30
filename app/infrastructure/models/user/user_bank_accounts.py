from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class UserBankAccountModel(Base):
    __tablename__ = "user_bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # A user can currently have only one bank account (BR-6)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bank_account_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"))





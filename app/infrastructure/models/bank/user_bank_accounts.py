from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, ValidityMixin

class UserBankAccountModel(Base, ValidityMixin):
    __tablename__ = "user_bank_accounts"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    bank_account_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"))
    
    
    
    
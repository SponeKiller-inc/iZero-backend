from sqlalchemy import (
    Column, 
    Integer, 
    String,  
    UniqueConstraint, 
    CheckConstraint, 
    or_,
)

from app.database.base import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    provider = Column(String, nullable=False, default="local")
    client_id = Column(String)
    email = Column(String, nullable=False)
    password = Column(String)
    
    __table_args__ = (
        CheckConstraint(
             or_(provider == 'local', client_id.isnot(None)),
             name='chk_need_fill_client_id'
        ),
        CheckConstraint(
            or_(provider != 'local', password.isnot(None)),
            name="chk_need_fill_password"
        ),
    )
    
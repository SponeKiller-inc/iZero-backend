from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
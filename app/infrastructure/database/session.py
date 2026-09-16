from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def _session_scope():
    db = session_local()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# FastAPI dependency: wraps the generator into a context manager itself (Depends(get_db)).
get_db = _session_scope

# Plain `with db_session() as db:` for code outside FastAPI's dependency injection (e.g. middleware).
db_session = contextmanager(_session_scope)
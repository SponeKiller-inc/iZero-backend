from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from app.utils.config import settings
from app.utils.validation import validate_non_empty_str, validate_positive_int

pwd_context = CryptContext(
    schemes=[settings.pwd_context_scheme],
    deprecated="auto"
    )

def hash_password(password: str) -> str:
    """
    Create hash 
    
    Args:
        password (str): password
    
    Returns:
        str: hash
    """
    
    return pwd_context.hash(password)

def verify_hash(password: str, hash: str) -> bool:
    """
    Verify hash

    Args:
        password (str): password
        hash (str): hashed password

    Returns:
        bool: true = hash and password are identical
    """
    
    try:
        return pwd_context.verify(password, hash)
    except Exception as e:
        raise ValueError("Invalid hash format") from e

def create_UTC_exp_time(minutes: int) -> datetime:
    """
    Create expiration time

    Args:
        minutes (int): minutest to expiration
    
    Returns:
        datetime: time of expiration 
        (YYYY-MM-DD HH:MM:SS.ffffff±HH:MM)
    """
    
    expire = (
        datetime.now(timezone.utc) 
        + timedelta(minutes=minutes)
    )
    
    return expire
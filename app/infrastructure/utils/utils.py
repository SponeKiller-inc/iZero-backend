from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.utils.config import settings

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
        minutes (int): minutes to expiration 
            (if 0, expiration = now + 100ms)
    
    Returns:
        datetime: time of expiration 
            (YYYY-MM-DD HH:MM:SS.ffffff±HH:MM)
    """
    now = datetime.now(timezone.utc)
    
    if minutes == 0:
        delta = timedelta(milliseconds=100)
    else:
        delta = timedelta(minutes=minutes)
        
    return now + delta

def get_UTC_current_time() -> datetime:
    """
    Returns current utc time
    
    Returns:
        datetime: current time
            (YYYY-MM-DD HH:MM:SS.ffffff±HH:MM)
    """
    return datetime.now(timezone.utc)

async def extract_access_token(request: Request) -> str | None:
    """
    Extract auth token from Request
    
    Args:
        request (Request) : Fastapi request
    
    Returns:
        str or None: Access token or None if not present in header
    """
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
    
    return await oauth2_scheme(request)
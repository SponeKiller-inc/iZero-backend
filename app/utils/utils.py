from app.utils.config import settings
from passlib.context import CryptContext

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

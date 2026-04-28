from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

class TokenProvider:
    """
    Extracts auth token from Request.
    """
    _oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    @staticmethod
    async def extract_access_token(request: Request) -> str | None:
        """
        Extracts auth token from Request.
        
        Args:
            request (Request): FastAPI request.
        
        Returns:
            str | None: Access token or None if not present in header.
        """
        return await TokenProvider._oauth2_scheme(request)
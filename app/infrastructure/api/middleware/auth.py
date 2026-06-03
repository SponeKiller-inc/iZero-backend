from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import sentry_sdk

from app.application.exceptions.auth import AccessTokenProviderError
from app.infrastructure.services.token_provider import TokenProvider
from app.infrastructure.services.jwt_access_token_generator import JwtAccessTokenGenerator

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for authentication user
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        
        # 1. Extraction from RQ
        jwt_token = await TokenProvider.extract_access_token(request)
        
        if not jwt_token:
            request.state.user_id = None
            return await call_next(request)

        # 2. decode jwt token
        try:
            payload = JwtAccessTokenGenerator.decode(jwt_token) 
        except AccessTokenProviderError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"}
            )
            
        request.state.user_id = payload.user_id
         
        return await call_next(request)
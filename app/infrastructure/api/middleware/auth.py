from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.application.constants.security import SecurityConstants
from app.application.exceptions.auth import AccessTokenProviderError
from app.application.security.auth_context import AuthContext
from app.application.security.hash_context import HashContext
from app.infrastructure.services.jwt_access_token_generator import (
    JwtAccessTokenGenerator,
)
from app.infrastructure.services.token_provider import TokenProvider


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for authorization user
    """
    def __init__(self, app):
        super().__init__(app)
        self._access_token_generator = JwtAccessTokenGenerator(
            secret_key=SecurityConstants.ACCESS_TOKEN_SECRET_KEY,
            algorithm=SecurityConstants.ACCESS_TOKEN_ALGORITHM,
        )

    async def dispatch(self, request: Request, call_next):        
        request.state.user_id = None

        # Reset auth/permission contexts so a reused execution context can't
        # leak a previous user's identity into this (possibly anonymous) request
        AuthContext.clear()
        HashContext.clear()

        # 1. Extraction from RQ
        jwt_token = await TokenProvider.extract_access_token(request)
        
        if not jwt_token:
            return await call_next(request)

        # 2. decode jwt token
        try:
            payload = self._access_token_generator.decode(jwt_token)
        except AccessTokenProviderError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or expired token"}
            )
            
        AuthContext.set(payload.user_id)
        request.state.user_id = payload.user_id

        return await call_next(request)
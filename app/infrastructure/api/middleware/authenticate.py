from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.application.security.authenticate import Authenticate
from app.infrastructure.repositories.user.user_role import AlchemyUserRoleRepository
from app.infrastructure.database.session import get_db

class AuthenticateMiddleware(BaseHTTPMiddleware):
    """
    Middleware for authentication user
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        
        db = next(get_db())
        user_role_repository = AlchemyUserRoleRepository(db)
        role_permission_repository = AlchemyRolePermissionRepository(db)
        time_provider = SystemTimeProvider()      
        
        authenticate = Authenticate(
            user_role_repository,
            role_permission_repository,
            time_provider
        )
         
        return await call_next(request)
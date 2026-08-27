from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.application.security.auth_context import AuthContext
from app.application.exceptions.auth import UnauthenticatedUserError
from app.infrastructure.services.time_provider import SystemTimeProvider
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.application.security.authenticate import Authenticate
from app.infrastructure.repositories.user.user_role import AlchemyUserRoleRepository
from app.infrastructure.repositories.auth.role_permission import AlchemyRolePermissionRepository
from app.infrastructure.database.session import get_db

class AuthenticateMiddleware(BaseHTTPMiddleware):
    """
    Middleware for authentication user
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        
        if AuthContext.get() is None:
            return await call_next(request)

        db = next(get_db())
        user_role_repository = AlchemyUserRoleRepository(db)
        role_permission_repository = AlchemyRolePermissionRepository(db)
        time_provider = SystemTimeProvider()      
        
        authenticate = Authenticate(
            user_role_repository,
            role_permission_repository,
            time_provider
        )

        try:
            authenticate.execute(AuthContext.get())
        except UnauthenticatedUserError as e:
            return JSONResponse(
                content=ResponseContainer(
                    message_id=MessageId.AUTH_NOT_AUTHENTICATED,
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
         
        return await call_next(request)
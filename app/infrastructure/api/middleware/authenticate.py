from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match

from app.application.exceptions.auth import (
    ResourceForbiddenError,
    UnauthenticatedUserError,
)
from app.application.security.auth_context import AuthContext
from app.application.security.authenticate import Authenticate
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.database.session import db_session
from app.infrastructure.repositories.auth.role_permission import (
    AlchemyRolePermissionRepository,
)
from app.infrastructure.repositories.user.user import AlchemyUserRepository
from app.infrastructure.repositories.user.user_role import AlchemyUserRoleRepository
from app.infrastructure.services.time_provider import SystemTimeProvider


class AuthenticateMiddleware(BaseHTTPMiddleware):
    """
    Middleware for authentication user
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        
        if AuthContext.get() is None:
            return await call_next(request)

        try:
            with db_session() as db:
                user_repository = AlchemyUserRepository(db)
                user_role_repository = AlchemyUserRoleRepository(db)
                role_permission_repository = AlchemyRolePermissionRepository(db)
                time_provider = SystemTimeProvider()

                authenticate = Authenticate(
                    user_repository,
                    user_role_repository,
                    role_permission_repository,
                    time_provider
                )

                authenticate.execute(
                    AuthContext.get(),
                    self._target_user_id(request),
                )
        except UnauthenticatedUserError:
            return JSONResponse(
                content=ResponseContainer(
                    message_id=MessageId.AUTH_NOT_AUTHENTICATED,
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except ResourceForbiddenError:
            return JSONResponse(
                content=ResponseContainer(
                    message_id=MessageId.AUTH_NOT_AUTHORIZED,
                ),
                status_code=status.HTTP_403_FORBIDDEN,
            )

        return await call_next(request)

    @staticmethod
    def _target_user_id(request: Request) -> int | None:
        """
        Resolve user_id path parameter of the route the request is heading to.
        Middleware runs before routing, so the routes are matched the same way the router does.

        Args:
            request: Incoming request

        Returns:
            Target user id or None if the route has no user_id
        """
        for route in request.app.router.routes:
            match, child_scope = route.matches(request.scope)
            print(match.value)
            print(child_scope)
            if match == Match.FULL:
                user_id = child_scope.get("path_params", {}).get("user_id")
                return int(user_id) if user_id and user_id.isdigit() else None

        return None
from fastapi import APIRouter

from app.infrastructure.services.route_security import RouteSecurityProvider
from .endpoints import user
from .endpoints import auth
from .endpoints import token
from .endpoints import module_group



router = APIRouter(prefix="/api/v1")

# Non - Secure Routes
router.include_router(auth.router)
router.include_router(token.router)

# Secure Routes
RouteSecurityProvider.register_secure_router(router, user.router)
RouteSecurityProvider.register_secure_router(router, module_group.router)
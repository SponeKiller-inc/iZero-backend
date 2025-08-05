from fastapi import APIRouter

from .router_utils import include_secure_router
from .endpoints import user
from .endpoints import token
from .endpoints import module



router = APIRouter(prefix="/api/v1")

# Non - Secure Routes
router.include_router(user.router)
router.include_router(token.router)

# Secure Routes
include_secure_router(router, module.router)
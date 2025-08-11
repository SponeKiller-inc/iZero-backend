from fastapi import APIRouter

from .router_utils import include_secure_router
from .endpoints import user
from .endpoints import auth
from .endpoints import token
from .endpoints import modul_group



router = APIRouter(prefix="/api/v1")

# Non - Secure Routes
router.include_router(auth.router)
router.include_router(token.router)

# Secure Routes
include_secure_router(router, user.router)
include_secure_router(router, modul_group.router)
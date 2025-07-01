from fastapi import APIRouter

from .endpoints import user
from .endpoints import token



router = APIRouter(prefix="/api/v1")

# Non - Secure Routes
router.include_router(user.router)
router.include_router(token.router)
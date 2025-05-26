from fastapi import APIRouter

from .endpoints import user



router = APIRouter(prefix="/api/v1")

# Non - Secure Routes
router.include_router(user.router)
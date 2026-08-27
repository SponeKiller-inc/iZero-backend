from fastapi import APIRouter

from .endpoints import user



router = APIRouter(prefix="/api")

router.include_router(user.router)
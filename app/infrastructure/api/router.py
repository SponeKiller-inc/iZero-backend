from fastapi import APIRouter

from .endpoints import auth, module, user

router = APIRouter(prefix="/api")

router.include_router(user.router)
router.include_router(auth.router)
router.include_router(module.router)
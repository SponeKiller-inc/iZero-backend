from fastapi import APIRouter

from .endpoints import address, auth, lookup, module, user

router = APIRouter(prefix="/api")

router.include_router(user.router)
router.include_router(auth.router)
router.include_router(module.router)
router.include_router(address.router)
router.include_router(lookup.router)

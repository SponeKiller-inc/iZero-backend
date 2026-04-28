from fastapi import APIRouter, Depends

from app.infrastructure.api.v1.dependencies.permission import verify_and_store_user

class RouteSecurityProvider:
    """
    Router security for API endpoints.
    """
    
    _auth_dependency = Depends(verify_and_store_user)

    @staticmethod
    def register_secure_router(main_router: APIRouter, subrouter: APIRouter) -> None:
        """
        Registers a subrouter in the main router with mandatory authentication.

        Args:
            main_router (APIRouter): The main router.
            subrouter (APIRouter): The subrouter to register.
        """
        main_router.include_router(
            subrouter,
            dependencies=[RouteSecurityProvider._auth_dependency]
        )
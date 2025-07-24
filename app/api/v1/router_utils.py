from fastapi import APIRouter, Depends
from .dependencies.permission import verify_and_store_user

def include_secure_router(main_router: APIRouter, subrouter: APIRouter) -> None:
    """
    Include a secure router with token verification.
    
    Args:
        main_router (APIRouter): The main router to include the subrouter in.
        subrouter (APIRouter): The subrouter to be included.

    """
    main_router.include_router(
        subrouter,
        dependencies=[Depends(verify_and_store_user)]
    )


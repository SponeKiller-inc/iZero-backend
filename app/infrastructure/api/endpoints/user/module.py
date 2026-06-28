from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.api.dependencies.security import verify_user_owns_resource


router = APIRouter(tags=["user-module"])


@router.get(
    "/{user_id}/modules", 
    response_model=Dict[str, List[str]], 
    status_code=status.HTTP_200_OK
)
async def get_user_modules(
    user_id: int,
    module_service: ModuleService = Depends(ModuleDependencies)
):
    try:
        return module_service.retrieve_user_modules(user_id)
    except UserModuleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user modules found",
        )
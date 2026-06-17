from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.api.v1.schemas.user import UserModuleIn
from app.domain.entity.module2 import ModuleService
from app.infrastructure.api.v1.dependencies.security import verify_user_owns_resource
from app.infrastructure.api.v1.dependencies.module import ModuleDependencies
from app.domain.modules.exceptions.module import (
    UserModuleNotFoundError,
    UserModuleNotAssignedError
)

router = APIRouter(tags=["user-module"], dependencies=[Depends(verify_user_owns_resource)])

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
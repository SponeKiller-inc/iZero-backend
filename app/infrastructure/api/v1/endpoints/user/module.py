from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
import sentry_sdk

from app.infrastructure.api.v1.schemas.user import UserModuleIn
from app.domain.services.module import ModuleService
from app.infrastructure.api.v1.dependencies.security import verify_user_owns_resource

from app.infrastructure.api.v1.dependencies.module import ModuleDependencies
from app.domain.exceptions.entity.module import (
    UserModuleNotFoundError,
    UserModuleNotAssignedError
)
from app.domain.exceptions.entity.module import ModuleServiceError

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
    except ModuleServiceError as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Something went wrong, while retrieving user modules"
                "please try again later"
            )
        )

@router.post("/{user_id}/modules", status_code=status.HTTP_201_CREATED)
async def assign_module_to_user(
    user_id: int,
    module: UserModuleIn,
    module_service: ModuleService = Depends(ModuleDependencies)
):
    try:
        module_service.assign_module_to_user(
            user_id, 
            module.module_id, 
            module.valid_from, 
            module.valid_to
        )
    except UserModuleNotAssignedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid data, module not exists or "
                "is active in requested period"
            )
        )
    except ModuleServiceError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Something went wrong, assigning module to user"
                "please try again later"
            )
        )
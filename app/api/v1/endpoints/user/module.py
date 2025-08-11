from fastapi import APIRouter, Depends, HTTPException, status, Request
import sentry_sdk

from ...schemas.user import UserModuleOut, UserModuleIn
from app.services.module import ModuleService
from ...dependencies.security import verify_user_owns_resource

from app.api.v1.dependencies.module import ModuleDependencies
from app.exceptions.domain.module import (
    UserModuleNotFoundError,
    UserModuleNotAssignedError
)
from app.exceptions.infrastucture.domain import ModuleServiceError

router = APIRouter(tags=["module"], dependencies=[verify_user_owns_resource])

@router.get(
    "/{user_id}/modules", 
    response_model=UserModuleOut, 
    status_code=status.HTTP_201_CREATED
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
    except UserModuleNotAssignedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid data, module not exists or "
                "is active in requested period"
            )
        )
    except ModuleService as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Something went wrong, assigning module to user"
                "please try again later"
            )
        )
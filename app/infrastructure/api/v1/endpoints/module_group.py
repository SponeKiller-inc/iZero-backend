from fastapi import APIRouter, Depends, HTTPException, status
import sentry_sdk

from app.infrastructure.api.v1.schemas.module_group import ModuleGroupIn, ModuleIn
from app.infrastructure.api.v1.dependencies.role_access import require_role
from app.domain.services.module import ModuleService
from app.infrastructure.api.v1.dependencies.module import ModuleDependencies
from app.domain.exceptions.entity.module import ModuleGroupNotCreatedError, ModuleNotCreatedError
from app.domain.exceptions.entity.module import ModuleServiceError

router = APIRouter(prefix="/module_groups", tags=["module_group"])

@router.post(
    "", 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[require_role("admin")]
)
async def create_module_group(
    module_group: ModuleGroupIn,
    module_service: ModuleService = Depends(ModuleDependencies)
):
    try:
        module_service.create_module_group(module_group.name)
    except ModuleGroupNotCreatedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data"
        )
    except ModuleServiceError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Something went wrong while creating module group, "
                "please try again later"
            )
        )

@router.post(
    "/{module_group_id}/modules", 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[require_role("admin")]
)
async def create_module(
    module_group_id: int,
    module: ModuleIn,
    module_service: ModuleService = Depends(ModuleDependencies)
):
    try:
        module_service.create_module(module.name, module_group_id)
    except ModuleNotCreatedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or module group not exists"
        )
    except ModuleServiceError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Something went wrong while creating module, "
                "please try again later"
            )
        )
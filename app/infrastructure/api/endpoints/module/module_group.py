from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.api.v1.schemas.module_group import ModuleGroupIn, ModuleIn
from app.infrastructure.api.v1.dependencies.role_access import require_role
from app.domain.entity.module2 import ModuleService
from app.infrastructure.api.v1.dependencies.module import ModuleDependencies
from app.domain.modules.exceptions.module import (
    ModuleGroupNotCreatedError,
    ModuleNotCreatedError,
)

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

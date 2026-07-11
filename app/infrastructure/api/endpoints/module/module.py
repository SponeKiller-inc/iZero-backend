from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post(
    "", 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[require_role("admin")]
)
async def create_module(
    module: ModuleIn,
    module_service: ModuleService = Depends(ModuleDependencies)
):

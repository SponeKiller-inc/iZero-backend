from fastapi import APIRouter, Depends, HTTPException, status
import sentry_sdk

from ..schemas.module_group import ModuleGroupIn, ModuleIn
from app.services.module import ModuleService

from app.api.v1.dependencies.module import ModuleDependencies
from app.exceptions.domain.module import ModuleGroupNotCreatedError

router = APIRouter(prefix="/module_groups", tags=["authentications"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_module_group(
    module_group: ModuleGroupIn,
    module_service: ModuleService = Depends(ModuleDependencies)
):
    try:
        module_service.create_module_group(module_group.name)
    except GoogleUserExistsError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except RegistrationError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later"
        )

@router.post("/google", status_code=status.HTTP_201_CREATED)
async def create_module(
    user: schema.GoogleRegistrationIn,
    user_service: UserService = Depends(UserDependencies)
):
    try:
        user_service.register_user_google(user.jwt_token)
    except GoogleUserExistsError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except RegistrationError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later"
        )
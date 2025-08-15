from fastapi import APIRouter, Depends, HTTPException, status
import sentry_sdk

from ..schemas import auth as schema
from app.services.user import UserService

from app.api.v1.dependencies.user import UserDependencies
from app.exceptions.domain.user import (
    LocalUserExistsError,
    GoogleUserExistsError,
    RegistrationError
)

router = APIRouter(prefix="/auth", tags=["authentications"])

@router.post("/local", status_code=status.HTTP_201_CREATED)
async def register_local(
    user: schema.LocalRegistrationIn,
    user_service: UserService = Depends(UserDependencies)
):
    try:
        user_service.register_user_local(
            user.email,
            user.password
        )
    except LocalUserExistsError as e:
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
async def register_google(
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
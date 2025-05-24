from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas import user as schema
from app.services.user_service import UserService
from app.api.dependencies import get_user_service
from app.exceptions.domain import (
    LocalUserExistsError,
    GoogleUserExistsError,
    RegistrationError
)

router = APIRouter(prefix="/users", tags=["authentications"])

@router.post("/local", status_code=status.HTTP_201_CREATED)
async def register(
    user: schema.LocalRegistrationIn,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user_service.register_user_local(
            user.email,
            user.password
        )
    except LocalUserExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except RegistrationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later"
        )

@router.post("/google", status_code=status.HTTP_201_CREATED)
async def register(
    user: schema.GoogleRegistrationIn,
    user_service: UserService = Depends(get_user_service)
):
    try:
        user_service.register_user_google(user.jwt_token)
    except GoogleUserExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except RegistrationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later"
        )
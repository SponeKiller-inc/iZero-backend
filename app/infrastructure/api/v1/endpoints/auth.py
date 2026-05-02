from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.api.v1.schemas import auth as schema
from app.domain.entity.user import UserService

from app.infrastructure.api.v1.dependencies.user import UserDependencies
from app.domain.exceptions.entity.user import (
    LocalUserExistsError,
    GoogleUserExistsError,
    
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

@router.post("/google", status_code=status.HTTP_201_CREATED)
async def register_google(
    user: schema.GoogleRegistrationIn,
    user_service: UserService = Depends(UserDependencies)
):
    try:
        user_service.register_user_google(user.jwt_token)
    except GoogleUserExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
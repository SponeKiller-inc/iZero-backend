from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.use_cases.users.register_local import RegisterLocal
from app.application.use_cases.users.register_oauth import RegisterOauth
from app.application.dto.user.registration import RegistrationLocalIn, RegistrationOauthIn
from app.application.exceptions.auth import IdentityProviderError
from app.application.exceptions.user import (
    RegisterLocalError,
    RegisterOauthError,
    
)
from app.infrastructure.database.session import get_db
from app.infrastructure.api.schemas import user as schema
from app.infrastructure.services.passlib_password_hasher import PasslibPasswordHasher
from app.infrastructure.repositories.user.user import AlchemyUserRepository
from app.infrastructure.services.time_provider import SystemTimeProvider
from app.infrastructure.providers.auth_google import GoogleIdentityProvider
from app.infrastructure.config import settings



router = APIRouter(prefix="/user", tags=["user"])

@router.post("/local", status_code=status.HTTP_201_CREATED)
async def register_local(
    user: schema.RegistrationLocalIn,
    db: Session = Depends(get_db)
):
    # Inicialize registration local
    user_repository = AlchemyUserRepository(db)
    user_role_repository = AlchemyUserRepository(db)
    password_hasher = PasslibPasswordHasher()
    time_provider = SystemTimeProvider()

    register = RegisterLocal(
        user_repository,
        user_role_repository,
        password_hasher,
        time_provider,
    )

    dto = RegistrationLocalIn(
        email=user.email,
        password=user.password,
    )

    # registration
    try:
        register.execute(dto)
    except RegisterLocalError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

@router.post("/google", status_code=status.HTTP_201_CREATED)
async def register_google(
    user: schema.RegistrationOauthIn,
    db: Session = Depends(get_db)
):
    # Inicialize registration oauth
    user_repository = AlchemyUserRepository(db)
    user_role_repository = AlchemyUserRepository(db)
    identity_provider = GoogleIdentityProvider(
        client_id=settings.GOOGLE_CLIENT_ID
    )
    time_provider = SystemTimeProvider()

    register = RegisterOauth(
        user_repository,
        user_role_repository,
        identity_provider,
        time_provider,
    )

    dto = RegistrationOauthIn(
        token = user.jwt_token
    )

    # registration
    try:
        register.execute(dto)
    except RegisterOauthError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except IdentityProviderError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google authentication failed"
        )
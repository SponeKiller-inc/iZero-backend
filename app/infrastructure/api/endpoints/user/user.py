from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.dto.user.registration import (
    RegistrationLocalIn,
    RegistrationOauthIn,
)
from app.application.exceptions.auth import IdentityProviderError
from app.application.exceptions.user import (
    RegisterLocalError,
    RegisterOauthError,
    UserCannotBeDeletedError,
    UserDeleteForbiddenError,
    UserNotFoundError,
)
from app.application.use_cases.users.delete_user import DeleteUser
from app.application.use_cases.users.register_local import RegisterLocal
from app.application.use_cases.users.register_oauth import RegisterOauth
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.api.schemas.user import user as schema
from app.infrastructure.config import settings
from app.infrastructure.database.session import get_db
from app.infrastructure.providers.auth_google import GoogleIdentityProvider
from app.infrastructure.repositories.user.user import AlchemyUserRepository
from app.infrastructure.repositories.user.user_role import AlchemyUserRoleRepository
from app.infrastructure.services.passlib_password_hasher import PasslibPasswordHasher
from app.infrastructure.services.time_provider import SystemTimeProvider

router = APIRouter()

@router.post(
    "/local",
    response_model=ResponseContainer[None],
    status_code=status.HTTP_201_CREATED,
)
async def register_local(
    user: schema.RegistrationLocalSchemaIn,
    db: Session = Depends(get_db)
):
    # Initialize registration local
    user_repository = AlchemyUserRepository(db)
    user_role_repository = AlchemyUserRoleRepository(db)
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
    except RegisterLocalError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.USER_ALREADY_EXISTS),
            status_code=status.HTTP_409_CONFLICT,
        )

    return ResponseContainer()

@router.post(
    "/google",
    response_model=ResponseContainer[None],
    status_code=status.HTTP_201_CREATED,
)
async def register_google(
    user: schema.RegistrationOauthSchemaIn,
    db: Session = Depends(get_db)
):
    # Initialize registration oauth
    user_repository = AlchemyUserRepository(db)
    user_role_repository = AlchemyUserRoleRepository(db)
    identity_provider = GoogleIdentityProvider(
        client_id=settings.google_oauth_client_id
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
    except RegisterOauthError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.USER_ALREADY_EXISTS),
            status_code=status.HTTP_409_CONFLICT,
        )
    except IdentityProviderError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.AUTH_IDENTITY_PROVIDER_FAILED),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return ResponseContainer()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_repository = AlchemyUserRepository(db)

    delete = DeleteUser(user_repository)

    try:
        delete.execute(user_id)
    except UserDeleteForbiddenError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.AUTH_NOT_AUTHORIZED),
            status_code=status.HTTP_403_FORBIDDEN,
        )
    except UserNotFoundError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.USER_NOT_FOUND),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except UserCannotBeDeletedError:
        return JSONResponse(
            content=ResponseContainer(message_id=MessageId.USER_CANNOT_BE_DELETED),
            status_code=status.HTTP_409_CONFLICT,
        )

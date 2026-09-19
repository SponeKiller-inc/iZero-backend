from fastapi import APIRouter, Response, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.application.use_cases.auth.login_local import LoginLocal
from app.application.use_cases.auth.login_google import LoginGoogle
from app.application.dto.auth.login_local import LoginLocalIn
from app.application.dto.auth.login_google import LoginGoogleIn
from app.application.exceptions.auth import InvalidCredentialsError, IdentityProviderError
from app.application.exceptions.user import UserNotFoundError
from app.application.constants.security import SecurityConstants
from app.infrastructure.api.schemas.token import TokenOut, GoogleTokenIn
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.user.user import AlchemyUserRepository
from app.infrastructure.repositories.auth.refresh_token import AlchemyRefreshTokenRepository
from app.infrastructure.services.passlib_password_hasher import PasslibPasswordHasher
from app.infrastructure.services.jwt_access_token_generator import JwtAccessTokenGenerator
from app.infrastructure.services.refresh_token_generator import RefreshTokenGenerator
from app.infrastructure.services.csrf_token_generator import CsrfTokenGenerator
from app.infrastructure.services.time_provider import SystemTimeProvider
from app.infrastructure.providers.auth_google import GoogleIdentityProvider
from app.infrastructure.config import settings

router = APIRouter(prefix="/token", tags=["authentications"])

@router.post("/local", response_model=TokenOut)
async def local_login(
    response: Response,
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenOut:
    # Initialize local login
    user_repository = AlchemyUserRepository(db)
    refresh_token_repository = AlchemyRefreshTokenRepository(db)
    password_hasher = PasslibPasswordHasher()
    access_token_generator = JwtAccessTokenGenerator(
        secret_key=SecurityConstants.ACCESS_TOKEN_SECRET_KEY,
        algorithm=SecurityConstants.ACCESS_TOKEN_ALGORITHM,
    )
    refresh_token_generator = RefreshTokenGenerator()
    csrf_token_generator = CsrfTokenGenerator()
    time_provider = SystemTimeProvider()

    login_local = LoginLocal(
        user_repository,
        refresh_token_repository,
        password_hasher,
        access_token_generator,
        refresh_token_generator,
        csrf_token_generator,
        time_provider,
    )

    dto = LoginLocalIn(
        email=user_credentials.username,
        password=user_credentials.password,
        session_id=request.state.session_id,
    )

    # login
    try:
        result = login_local.execute(dto)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    response.set_cookie(key="refresh_token",
                        value=result.refresh_token,
                        httponly=True,
                        secure=True,
                        samesite="strict",
                        expires=result.refresh_token_expires_at)

    response.set_cookie(key="csrf_token",
                        value=result.csrf_token,
                        secure=True,
                        samesite="strict")

    return TokenOut(
        access_token=result.access_token,
        token_type=result.access_token_type,
    )

@router.post("/google", response_model=TokenOut)
async def google_login(
    response: Response,
    request: Request,
    user_credentials: GoogleTokenIn,
    db: Session = Depends(get_db),
) -> TokenOut:
    # Initialize google login
    user_repository = AlchemyUserRepository(db)
    refresh_token_repository = AlchemyRefreshTokenRepository(db)
    identity_provider = GoogleIdentityProvider(
        client_id=settings.google_oauth_client_id,
    )
    access_token_generator = JwtAccessTokenGenerator(
        secret_key=SecurityConstants.ACCESS_TOKEN_SECRET_KEY,
        algorithm=SecurityConstants.ACCESS_TOKEN_ALGORITHM,
    )
    refresh_token_generator = RefreshTokenGenerator()
    csrf_token_generator = CsrfTokenGenerator()
    time_provider = SystemTimeProvider()

    login_google = LoginGoogle(
        user_repository,
        refresh_token_repository,
        identity_provider,
        access_token_generator,
        refresh_token_generator,
        csrf_token_generator,
        time_provider,
    )

    dto = LoginGoogleIn(
        token=user_credentials.jwt_token,
        session_id=request.state.session_id,
    )

    # login
    try:
        result = login_google.execute(dto)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    except IdentityProviderError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google authentication failed",
        )

    response.set_cookie(key="refresh_token",
                        value=result.refresh_token,
                        httponly=True,
                        secure=True,
                        samesite="strict",
                        expires=result.refresh_token_expires_at)

    response.set_cookie(key="csrf_token",
                        value=result.csrf_token,
                        secure=True,
                        samesite="strict")

    return TokenOut(
        access_token=result.access_token,
        token_type=result.access_token_type,
    )

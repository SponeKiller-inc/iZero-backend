from fastapi import APIRouter, Response, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import sentry_sdk

from ..schemas.token import TokenOut
from ..dependencies.token import TokenDependencies
from ..dependencies.session import SessionDependencies
from ..dependencies.auth import AuthDependencies
from app.services.token import TokenService
from app.services.session import SessionService
from app.services.auth import AuthService
from app.utils.utils import extract_access_token

from app.exceptions.domain.user import (
    UserNotVerifiedError,
    UserVerificationError,
    LocalUserNotVerifiedError,
    LocalUserVerificationError,
)
from app.exceptions.domain.token import (
    RefreshTokenServiceError,
    AccessTokenServiceError,
    CSRFTokenCreationError,
)
from app.exceptions.domain.session import GetSessionServiceError

router = APIRouter(prefix="/token",
                   tags=["authentications"])

@router.post("/local", response_model=TokenOut)
async def local_login(
    response: Response,
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(AuthDependencies),
    session_service: SessionService = Depends(SessionDependencies),
    token_service: TokenService = Depends(TokenDependencies),
) -> TokenOut:
    
    try:
        user_id = auth_service.authenticate_user_local(
            user_credentials.username, 
            user_credentials.password,
        )
    except LocalUserNotVerifiedError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    except LocalUserVerificationError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later",
        )
        
    try:
        session = session_service.retrieve_session(request.state.sid)
        
        access_token = token_service.create_access_token(user_id)
        refresh_token, refresh_token_expires = (
            token_service.create_refresh_token(session.id)
        )
        csrf_token = token_service.create_csrf_token()
    except (
        GetSessionServiceError,
        AccessTokenServiceError, 
        RefreshTokenServiceError,
        CSRFTokenCreationError,
    ) as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later",
        )
    
    
    response.set_cookie(key="refresh_token",
                        value=f"{refresh_token}",
                        httponly=True,
                        secure=True,
                        samesite="strict",
                        expires=refresh_token_expires)
    
    response.set_cookie(key="csrf_token",
                        value=f"{csrf_token}",
                        secure=True,
                        samesite="strict")
    
    return {"access_token": access_token,   
            "token_type": "bearer"}

@router.get("/me", status_code=status.HTTP_204_NO_CONTENT)
async def me(
    auth_service: AuthService = Depends(AuthDependencies),
    token: str = Depends(extract_access_token),
) -> None:
    try:
        auth_service.authenticate_user_token(token)
    except UserNotVerifiedError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    except UserVerificationError as e:
        sentry_sdk.capture_exception(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later",
        )
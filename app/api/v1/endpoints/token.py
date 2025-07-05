from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from ..schemas.token import Token
from ..dependencies.token import TokenDependencies
from ..dependencies.auth import AuthDependencies
from app.services.token import TokenService
from app.services.auth import AuthService
from app.exceptions.domain.user import (
    LocalUserNotVerifiedError,
    LocalUserVerificationError,
)
from app.exceptions.domain.token import (
    RefreshTokenServiceError,
    AccessTokenServiceError,
    CSRFTokenCreationError
)

router = APIRouter(prefix="/token",
                   tags=["authentications"])

@router.post("/local", response_model=Token)
async def local_login(
    response: Response,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(AuthDependencies),
    token_service: TokenService = Depends(TokenDependencies),
) -> Token:
    
    try:
        user_id = auth_service.authenticate_user_local(
            user_credentials.username, 
            user_credentials.password,
        )
    except LocalUserNotVerifiedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    except LocalUserVerificationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, please try again later",
        )
        
    try:
        access_token = token_service.create_access_token(user_id)
        refresh_token, refresh_token_expires = token_service.create_refresh_token()
        csrf_token = token_service.create_csrf_token()
    except (
        AccessTokenServiceError, 
        RefreshTokenServiceError,
        CSRFTokenCreationError,
    ):
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
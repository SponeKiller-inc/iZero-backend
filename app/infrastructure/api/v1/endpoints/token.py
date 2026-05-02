from fastapi import APIRouter, Response, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.infrastructure.api.v1.schemas.token import TokenOut, GoogleTokenIn
from app.infrastructure.api.v1.dependencies.token import TokenDependencies
from app.infrastructure.api.v1.dependencies.session import SessionDependencies
from app.infrastructure.api.v1.dependencies.auth import AuthDependencies
from app.domain.entity.token import TokenService
from app.domain.entity.session import SessionService
from app.domain.entity.auth2 import AuthService
from app.infrastructure.services.token_provider import TokenProvider

from app.domain.exceptions.entity.user import (
    UserNotVerifiedError,
    LocalUserNotVerifiedError,
    GoogleUserNotVerifiedError,
)

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
        
    session = session_service.retrieve_session(request.state.sid)
    
    access_token = token_service.create_access_token(user_id)
    refresh_token, refresh_token_expires = (
        token_service.create_refresh_token(session.id)
    )
    csrf_token = token_service.create_csrf_token()
    
    
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

@router.post("/google", response_model=TokenOut)
async def google_login(
    response: Response,
    request: Request,
    user_credentials: GoogleTokenIn,
    auth_service: AuthService = Depends(AuthDependencies),
    session_service: SessionService = Depends(SessionDependencies),
    token_service: TokenService = Depends(TokenDependencies),
) -> TokenOut:
    
    try:
        user_id = auth_service.authenticate_user_google(
            user_credentials.jwt_token, 
        )
    except GoogleUserNotVerifiedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
        
    
    session = session_service.retrieve_session(request.state.sid)
    
    access_token = token_service.create_access_token(user_id)
    refresh_token, refresh_token_expires = (
        token_service.create_refresh_token(session.id)
    )
    csrf_token = token_service.create_csrf_token()
    
    
    
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
    token: str = Depends(TokenProvider.extract_access_token),
) -> None:
    try:
        auth_service.authenticate_user_token(token)
    except UserNotVerifiedError as e:  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
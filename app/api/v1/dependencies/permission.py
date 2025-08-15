from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import sentry_sdk

from app.services.user import UserService
from app.api.v1.dependencies.user import UserDependencies
from app.utils.config import settings
from app.exceptions.domain.user import UserNotFoundError
from app.exceptions.infrastucture.domain import UserServiceError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/local")

async def verify_and_store_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(UserDependencies)
):
    """
    Verify the access token and store the user in the request state.
    
    Args:
        request (Request): The HTTP request object.
        token (str):  JWT-access token
        user_service (User_Service )
    Raises:
        HTTPException: 
            If token expired or invalid (401) 
            If the user is not found (404)
            if server side error (500)
    """
    
    try:
        payload = jwt.decode(token,
                             settings.secret_key,
                             algorithms=settings.algorithm)
        
        user_id = payload.get("user_id", 0)

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your access token is missing user id",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            user_service.retrieve_user(user_id)
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except UserServiceError as e:
            sentry_sdk.capture_exception(e)
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Something went wrong while authorization, "
                    "please try again later"
                ),
                headers={"WWW-Authenticate": "Bearer"},
            ) 
    except JWTError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your access token is invalid or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    request.state.user_id = user_id
    
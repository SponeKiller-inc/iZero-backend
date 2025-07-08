from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import sentry_sdk

from .dependency.session import SessionDependencies
from app.services.session import SessionEventType
from app.utils.utils import extract_access_token

from app.exceptions.domain.session import (
    InicializeSessionServiceError, 
    LogSessionServiceError,
)
class SIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that initializes sessions and sets a session ID cookie.

    """
    def __init__(self, app):

        super().__init__(app)
        
        self.session_service = SessionDependencies()
    
    async def dispatch(self, request: Request, call_next):
        
        
        external_id = request.cookies.get("sid")
        user_agent = request.headers.get("user-agent")
        jwt_token = await extract_access_token(request)
        ip_address = request.client.host
        try:
            session_id, external_id = self.session_service.inicialize_session(
                external_id,
                jwt_token,
                ip_address,
                user_agent
            )
            
            self.session_service.record_session_event(
                session_id, 
                SessionEventType.SESSION_INITIALIZED
            )
        except (
            InicializeSessionServiceError,
            LogSessionServiceError,
        ) as e:
            sentry_sdk.capture_exception(e)
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content = {
                    "detail":
                        "Something went wrong while creating session. "
                        "Please try again later"
                }
            )
        # Store external session id to state
        # for use in endpoints
        request.state.sid = external_id
         
        response = await call_next(request)

        if request.cookies.get("sid") is None:
            # Set the sid cookie if it didn't exist
            response.set_cookie(key="sid", value=external_id, httponly=True)
        
        return response
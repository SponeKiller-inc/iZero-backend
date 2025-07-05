from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .dependency.session import SessionDependencies
from app.services.session import SessionEventType
from app.utils.utils import extract_access_token

from app.exceptions.domain.session import (
    InicializeSessionServiceError, 
    LogSessionServiceError,
)
class SIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that ensures each request has a session ID ('sid').

    Retrieves 'sid' from cookies or generates a new UUID, assigns it to
    `request.state.sid` to work with in endpoints, and sets the cookie 
    on the response if it was missing.
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
            session_id = self.session_service.inicialize_session(
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
        ):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Something went wrong please try again later"
                }
            )
                
        response = await call_next(request)

        if request.cookies.get("sid") is None:
            # Set the sid cookie if it didn't exist
            response.set_cookie(key="sid", value=external_id, httponly=True)
        
        return response
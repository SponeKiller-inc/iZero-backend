from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.application.dto.sessions.initialize_session import InitializeSessionIn
from app.application.use_cases.sessions.initialize_session import InitializeSession
from app.application.exceptions.user import UserNotFoundError
from app.infrastructure.services.time_provider import SystemTimeProvider
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.session import AlchemySessionRepository
from app.infrastructure.repositories.user import AlchemyUserRepository



class SIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that initializes sessions and sets a session ID cookie.

    """
    def __init__(self, app):

        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        external_id = request.cookies.get("sid")
        user_agent = request.headers.get("user-agent")
        user_id = request.state.user_id
        ip_address = request.client.host

        # Initialize application services
        db = next(get_db())
        session_repository = AlchemySessionRepository(db)
        user_repository = AlchemyUserRepository(db)
        time_provider = SystemTimeProvider()
        
        session_service = InitializeSession(
            session_repository,
            user_repository,
            time_provider
        )
        
        session_dto = InitializeSessionIn(
            external_id=external_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        try:
            session = session_service.execute(session_dto)
        except UserNotFoundError as e:
            return JSONResponse(
                content={"message": "User not found"},
                status_code=400,
            )
        
        # Store external session id to state
        request.state.sid = session.external_id
         
        response = await call_next(request)

        if request.cookies.get("sid") is None:
            # Set the sid cookie if it didn't exist
            response.set_cookie(key="sid", value=session.external_id, httponly=True)
        
        return response
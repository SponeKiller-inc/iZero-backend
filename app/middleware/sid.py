from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class SIDMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        
        sid = request.cookies.get("sid") or str(uuid.uuid4())
        
        request.state.sid = sid
        
        response = await call_next(request)

        if request.cookies.get("sid") is None:
            # Set the sid cookie if it didn't exist
            response.set_cookie(key="sid", value=sid, httponly=True)
        
        return response
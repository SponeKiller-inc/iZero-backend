from fastapi import status
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk

from app.infrastructure.api.middleware.auth import AuthMiddleware
from app.infrastructure.api.middleware.authenticate import AuthenticateMiddleware
from app.infrastructure.api.middleware.sid import SIDMiddleware
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.api.schemas.base import ResponseContainer
from app.infrastructure.api.router import router
from app.infrastructure.config import settings
from app.application.exceptions.auth import AuthHashVerificationError

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    send_default_pii=True
)

app = FastAPI()

#Middleware

##CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins.split(","),
    allow_credentials=True,
    allow_methods=settings.cors_allow_methods.split(","),
    allow_headers=settings.cors_allow_headers.split(","),
)

##HTTP
app.add_middleware(AuthenticateMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(SIDMiddleware)


#Routing

##API v1
app.include_router(router)

#Global exceptions
@app.exception_handler(AuthHashVerificationError)
async def user_not_authorized_handler(request: Request, exc: AuthHashVerificationError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=ResponseContainer(
            message_id=MessageId.AUTH_NOT_ACCESS,
        )
    )

@app.exception_handler(Exception)
async def global_fallback_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc) 

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseContainer(
            message_id=MessageId.SYSTEM_INTERNAL_FAIL,
        ),        
    )
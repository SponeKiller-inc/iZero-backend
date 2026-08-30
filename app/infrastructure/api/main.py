from fastapi import status
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

from app.infrastructure.api.middleware.auth import AuthMiddleware
from app.infrastructure.api.middleware.authenticate import AuthenticateMiddleware
from app.infrastructure.api.middleware.sid import SIDMiddleware
from app.infrastructure.api.schemas.message_id import MessageId
from app.infrastructure.api.schemas.base import JSONResponse, ResponseContainer
from app.infrastructure.api.router import router
from app.infrastructure.config import settings
from app.application.exceptions.auth import AuthHashVerificationError

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    environment=settings.sentry_environment,
    traces_sample_rate=settings.sentry_traces_sample_rate,
    send_default_pii=settings.sentry_send_default_pii,
)

app = FastAPI()

#Middleware

##CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

##HTTP
# Starlette runs middleware in the reverse order they are added, so AuthMiddleware
# (which sets request.state.user_id) must be added last to execute first.
app.add_middleware(AuthenticateMiddleware)
app.add_middleware(SIDMiddleware)
app.add_middleware(AuthMiddleware)


#Routing

##API v1
app.include_router(router)

#Global exceptions
@app.exception_handler(AuthHashVerificationError)
async def user_not_authorized_handler(request: Request, exc: AuthHashVerificationError):
    return JSONResponse(
        content=ResponseContainer(message_id=MessageId.AUTH_NOT_ACCESS),
        status_code=status.HTTP_403_FORBIDDEN,
    )

@app.exception_handler(Exception)
async def global_fallback_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc) 

    return JSONResponse(
        content=ResponseContainer(message_id=MessageId.SYSTEM_INTERNAL_FAIL),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
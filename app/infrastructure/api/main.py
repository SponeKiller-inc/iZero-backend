from app.application.exceptions.auth import UserNotAuthorizedError
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk

from app.infrastructure.api.middleware.sid import SIDMiddleware
from app.infrastructure.api.router import router
from app.infrastructure.config import settings

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
app.add_middleware(SIDMiddleware)




#Routing

##API v1
app.include_router(router)

#Global exceptions
@app.exception_handler(UserNotAuthorizedError)
async def user_not_authorized_handler(request: Request, exc: UserNotAuthorizedError):
    return JSONResponse(
        status_code=403,
        content={"message": str(exc)}
    )

@app.exception_handler(Exception)
async def global_fallback_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc) 

    return JSONResponse(
        content={"message": "Internal server error. Administrators have been notified."},
        status_code=500,
    )
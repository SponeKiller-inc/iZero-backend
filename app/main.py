from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

from app.middleware.sid import SIDMiddleware
from app.api.v1 import routers as routers_v1
from app.utils.config import settings

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
app.include_router(routers_v1.router)


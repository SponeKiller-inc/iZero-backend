import os
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from dotenv import dotenv_values

_env_app = {
    **dotenv_values(Path(__file__).resolve().parents[3] / ".env.app"),
    **os.environ,
}


@dataclass(frozen=True)
class SecurityConstants:
    AUTH_SECRET: Final[str] = _env_app["AUTH_SECRET"]
    ACCESS_TOKEN_SECRET_KEY: Final[str] = _env_app["ACCESS_TOKEN_SECRET_KEY"]
    BEARER_TOKEN_TYPE: Final[str] = 'bearer'
    ACCESS_TOKEN_ALGORITHM: Final[str] = 'HS256'

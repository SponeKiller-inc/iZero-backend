from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    pwd_context_scheme: str
    user_module_expire_minutes: int
    cors_allow_origins: list[str]
    cors_allow_methods: list[str]
    cors_allow_headers: list[str]
    sentry_dsn: str
    sentry_environment: str = "development"
    sentry_traces_sample_rate: float = 0.0
    sentry_send_default_pii: bool = False
    google_oauth_client_id:str
    http_audit_sensitive_headers: list[str] = [
        "authorization", "cookie", "set-cookie", "x-api-key", "proxy-authorization",
    ]
    http_audit_sensitive_body_fields: list[str] = [
        "password", "new_password", "old_password", "current_password",
        "token", "access_token", "refresh_token", "id_token", "jwt_token",
        "client_secret", "secret", "csrf_token", "api_key", "authorization",
    ]
    http_audit_max_body_length: int = 10_000
    ruian_query_url: str
    ruian_page_size: int
    ruian_request_timeout_seconds: int
    ruian_max_retries: int = 3
    ruian_retry_backoff_seconds: float = 2.0
    

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      case_sensitive=False,
                                      extra = "ignore")

    @field_validator(
        "cors_allow_origins", "cors_allow_methods", "cors_allow_headers",
        "http_audit_sensitive_headers", "http_audit_sensitive_body_fields",
        mode="before",
    )
    @classmethod
    def _split(cls, value: str | list[str]) -> list[str]:
        """Parses a comma-separated .env value into trimmed, non-empty items."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def database_url(self) -> URL:
        """Postgres DSN with credentials escaped (safe against special characters)."""
        return URL.create(
            drivername="postgresql",
            username=self.database_username,
            password=self.database_password,
            host=self.database_hostname,
            port=self.database_port,
            database=self.database_name,
        )

        
settings = Settings()
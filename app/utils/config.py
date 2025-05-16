
from pydantic_settings import BaseSettings, SettingsConfigDict 


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    refresh_token_expire_minutes: str
    refresh_token_length: str
    csrf_token_length: str
    pwd_context_scheme: str
    cors_allow_origins: str
    cors_allow_methods: str
    cors_allow_headers: str
    sentry_dsn: str
    google_oauth_client_id:str
    

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      case_sensitive=False,
                                      extra = "ignore")
        
settings = Settings()
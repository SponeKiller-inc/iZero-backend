class TokenService:
    def __init__(self, repo: ITokenRepository) -> None:
        self.repo = repo
    
    def create_access_token(self, user_id: int) -> AccessToken:
        """Vytvoří entitu AccessToken."""
        try:
            expire = create_UTC_exp_time(int(settings.access_token_expire_minutes))
            data = {"user_id": user_id, "exp": expire}

            encoded_jwt = jwt.encode(
                data, 
                settings.secret_key, 
                algorithm=settings.algorithm
            )
            
            return AccessToken(
                token=encoded_jwt,
                user_id=user_id,
                expires_at=expire
            )
        except JWTError as e:
            raise AccessTokenServiceError from e
        
    def create_refresh_token(self, session_id: int) -> RefreshToken:
        """Vytvoří a uloží entitu RefreshToken."""
        try:
            expire = create_UTC_exp_time(int(settings.refresh_token_expire_minutes))
            token_value = secrets.token_hex(int(settings.refresh_token_length))
            
            # Vytvoření entity
            refresh_token = RefreshToken(
                session_id=session_id,
                token=token_value,
                expired_at=expire,
            )
        
            self.repo.create_refresh_token(refresh_token)
            return refresh_token
            
        except (RefreshTokenCreationError, ValueError, TypeError, CreateExecutionError) as e:
            raise RefreshTokenServiceError("Unable to generate refresh token") from e
            
    def create_csrf_token(self) -> CSRFToken:
        """Vytvoří entitu CSRFToken."""
        try:
            value = secrets.token_hex(int(settings.csrf_token_length))
            return CSRFToken(value=value)
        except (ValueError, TypeError) as e:
            raise CSRFTokenCreationError from e
    
    def verify_access_token(self, token: str) -> int:
        """Ověří token a vrátí ID uživatele."""
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm], # jwt.decode očekává list algoritmů
            )
            
            user_id = payload.get("user_id")
            if user_id is None:
                raise AccessTokenServiceError("Access token does not contain user id")
            
            return int(user_id)
        except (JWTError, ValueError) as e:
            raise AccessTokenServiceError("Not valid access token") from e
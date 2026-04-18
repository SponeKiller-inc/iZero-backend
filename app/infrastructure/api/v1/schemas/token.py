from pydantic import BaseModel

class GoogleTokenIn(BaseModel):
    jwt_token: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str
    
    
    
  
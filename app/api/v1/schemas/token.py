from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: int
    
class SessionUser(BaseModel):
    user_id: int
  
  
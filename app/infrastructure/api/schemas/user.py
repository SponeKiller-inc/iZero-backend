from datetime import datetime

from pydantic import BaseModel, EmailStr

class LocalRegistrationIn(BaseModel):
    email: EmailStr
    password: str

class GoogleRegistrationIn(BaseModel):
    jwt_token: str

class UserModuleIn(BaseModel):
    module_id: int
    valid_from: datetime
    valid_to: datetime
    
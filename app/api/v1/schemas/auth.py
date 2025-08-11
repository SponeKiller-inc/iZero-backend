from pydantic import BaseModel, EmailStr

class LocalRegistrationIn(BaseModel):
    email: EmailStr
    password: str

class GoogleRegistrationIn(BaseModel):
    jwt_token: str

   
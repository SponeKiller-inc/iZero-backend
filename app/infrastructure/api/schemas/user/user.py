from datetime import datetime

from pydantic import BaseModel, EmailStr


class RegistrationLocalSchemaIn(BaseModel):
    email: EmailStr
    password: str

class RegistrationOauthSchemaIn(BaseModel):
    jwt_token: str

class ChangePasswordSchemaIn(BaseModel):
    current_password: str
    new_password: str
    password_confirmation: str

class UserModuleSchemaIn(BaseModel):
    module_id: int
    valid_from: datetime
    valid_to: datetime
    
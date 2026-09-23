from pydantic import BaseModel, ConfigDict, Field


class GoogleTokenSchemaIn(BaseModel):
    jwt_token: str

class TokenSchemaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = Field(validation_alias="access_token_type")

"""
Pydantic Models for GenerateToken API's
"""
from pydantic import BaseModel
from typing import Optional
from schemas.schema_examples import (BASIC_GENERATE_TOKEN_RESPONSE_EXAMPLE)



class ResponseModel(BaseModel):
  access_token: str
  expires_in: str
  token_type: str
  refresh_token: str
  id_token: str
  project_id: str
  user_id: str


class GenerateTokenResponseModel(BaseModel):
  """Generate Token Response Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: ResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Token validated successfully",
            "data": BASIC_GENERATE_TOKEN_RESPONSE_EXAMPLE
        }
    }


class GenerateTokenRequestModel(BaseModel):
  refresh_token: str

  class Config():
    orm_mode = True
    schema_extra = {"example": {"refresh_token": "Afhfhh...........frtyhgjh"}}

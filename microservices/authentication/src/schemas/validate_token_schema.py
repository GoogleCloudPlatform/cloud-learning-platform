"""
Pydantic Models for ValidateToken API's
"""
from pydantic import BaseModel
from typing import List, Optional
from schemas.schema_examples import BASIC_VALIDATE_TOKEN_RESPONSE_EXAMPLE


# pylint: disable=line-too-long
class IdentityModel(BaseModel):
  email: List[str]


class FirebaseModel(BaseModel):
  identities: IdentityModel
  sign_in_provider: str


class ResponseModel(BaseModel):
  """data Pydantic Model"""
  name: Optional[str]
  picture: Optional[str]
  iss: str
  aud: str
  auth_time: int
  user_id: str
  sub: str
  iat: int
  exp: int
  email: str
  email_verified: bool
  firebase: FirebaseModel
  uid: str
  access_api_docs: bool
  user_type:str


class ValidateTokenResponseModel(BaseModel):
  """Validate Token Response Pydantic Model"""
  message: str = "Token validated successfully"
  success: bool = True
  data: ResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Token validated successfully",
            "data": BASIC_VALIDATE_TOKEN_RESPONSE_EXAMPLE
        }
    }

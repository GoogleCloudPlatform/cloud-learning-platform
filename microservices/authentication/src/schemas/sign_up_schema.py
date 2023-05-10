"""
Pydantic Model for Sign Up API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import (
    SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE,
    SIGN_UP_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE)

# pylint: disable=invalid-name
class SignUpWithCredentialsModel(BaseModel):
  """Sign Up with Credentials Input Pydantic Model"""
  email: str
  password: str

  class Config():
    orm_mode = True
    schema_extra = {"example": SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE}
    extra = "forbid"


class IDPSignUpWithCredentialsResponseModel(BaseModel):
  """Sign Up With Credentials Response Pydantic Model"""
  user_id: str
  kind: str
  localId: str
  email: str
  idToken: str
  refreshToken: str
  expiresIn: str
  session_id: str


class SignUpWithCredentialsResponseModel(BaseModel):
  """Sign Up With Credentials Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully signed up"
  data: IDPSignUpWithCredentialsResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully signed up",
            "data": SIGN_UP_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE
        }
    }

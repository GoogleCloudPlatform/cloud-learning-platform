"""
Pydantic Model for Sign In API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import (
    SIGN_IN_WITH_CREDENTIALS_API_INPUT_EXAMPLE,
    SIGN_IN_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE,
    SIGN_IN_WITH_TOKEN_RESPONSE_EXAMPLE)

# pylint: disable=invalid-name
class SignInWithCredentialsModel(BaseModel):
  """Sign In with Credentials Input Pydantic Model"""
  email: str
  password: str

  class Config():
    orm_mode = True
    schema_extra = {"example": SIGN_IN_WITH_CREDENTIALS_API_INPUT_EXAMPLE}
    extra = "forbid"


class IDPSignInWithCredentialsResponseModel(BaseModel):
  """Sign In With Credentials Response Pydantic Model"""
  user_id: str
  kind: str
  localId: str
  email: str
  displayName: str
  idToken: str
  registered: bool
  refreshToken: str
  expiresIn: str
  session_id: str


class SignInWithCredentialsResponseModel(BaseModel):
  """Sign In With Credentials Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully signed in"
  data: IDPSignInWithCredentialsResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully signed in",
            "data": SIGN_IN_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE
        }
    }


class IDPSignInWithTokenResponse(BaseModel):
  """Sign In With Token Response Pydantic Model"""
  user_id: str
  federatedId: str
  providerId: str
  email: str
  emailVerified: bool
  firstName: str
  fullName: str
  lastName: str
  photoUrl: str
  localId: str
  displayName: str
  idToken: str
  refreshToken: str
  expiresIn: str
  oauthIdToken: str
  rawUserInfo: str
  kind: str
  session_id: str


class SignInWithTokenResponseModel(BaseModel):
  """SignIn With Token Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully signed in"
  data: IDPSignInWithTokenResponse

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully signed in",
            "data": SIGN_IN_WITH_TOKEN_RESPONSE_EXAMPLE
        }
    }

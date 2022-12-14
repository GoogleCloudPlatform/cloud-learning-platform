"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import CREDENTIAL_JSON


class SectionDetails(BaseModel):
  """Course Detail model"""
  uuid: Optional[str]
  name: str
  description: str
  course_template: str
  cohort: str
  teachers_list: list


class SectionResponseModel(BaseModel):
  """Delete Course Template Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the course template"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the course template",
            "data": None
        }
    }


class CredentialKeys(BaseModel):
  """Credential model"""
  token: str
  refresh_token: str
  token_uri: str
  client_id: str
  client_secret: str
  scopes: list[str]
  expiry: str

  class Config():
    orm_mode = True
    schema_extra = {"example": CREDENTIAL_JSON}


class AddStudentToSectionModel(BaseModel):
  """Input Model to add student in section"""
  email: str
  credentials: CredentialKeys

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "email": "email@gmail.com",
            "credentials": CREDENTIAL_JSON
        }
    }


class AddStudentResponseModel(BaseModel):
  """Add Student Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Added the Student"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Added the Student",
            "data": None
        }
    }

class DeleteSectionResponseModel(BaseModel):
  """Delete section Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the section"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the section",
            "data": None
        }
    }

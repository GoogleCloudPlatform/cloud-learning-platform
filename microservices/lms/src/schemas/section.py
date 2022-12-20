"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import CREDENTIAL_JSON,SECTION_EXAMPLE


class Sections(BaseModel):
  """Sections Details """
  uuid : Optional[str]
  name:  Optional[str]
  section: Optional[str]
  description: Optional[str]
  classroom_id:Optional[str]
  classroom_code: Optional[str]
  teachers_list: Optional[list]
  is_deleted: Optional[bool]
  created_timestamp: Optional[str]
  last_updated_timestamp:Optional[str]
  deleted_at_timestamp: Optional[bool]
  id: Optional[str]
  key: Optional[str]
  course_template: Optional[str]
  cohort: Optional[str]

class SectionDetails(BaseModel):
  """Course Detail model"""
  uuid: Optional[str]
  name: str
  description: str
  course_template: str
  cohort: str
  teachers_list: list


class SectionListResponseModel(BaseModel):
  """Get a list of sections"""
  success: Optional[bool] = True
  message: Optional[str] = "Success list"
  data: Optional[list] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully send the list of  course ",
            "data": [SECTION_EXAMPLE]
        }
    }

class CreateSectiontResponseModel(BaseModel):
  """Create Section Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the cohort"
  data: Optional[SectionDetails]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the cohort",
           "section":SECTION_EXAMPLE
        }
    }

class GetSectiontResponseModel(BaseModel):
  """Get  Section Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Success"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Success",
           "data":SECTION_EXAMPLE
        }
    }


class UpdateResponseModel(BaseModel):
  """Update  Section Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Success"
  data: Optional[dict] = {}

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Section Updated successfully",
           "data":SECTION_EXAMPLE
        }
    }

class SectionResponseModel(BaseModel):
  """Get a list of sections"""
  success: Optional[bool] = True
  message: Optional[str] = "Success list"
  data: Optional[list] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully send the list of  course ",
            "data": []
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

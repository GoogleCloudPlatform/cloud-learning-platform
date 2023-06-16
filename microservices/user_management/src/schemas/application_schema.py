"""
Pydantic Model for Application API's
"""
from typing import List, Optional
from pydantic import BaseModel, Extra, StrictStr
from common.utils.custom_validator import BaseConfigModel
from schemas.schema_examples import (BASIC_APPLICATION_MODEL_EXAMPLE,
                                     FULL_APPLICATION_MODEL_EXAMPLE)


class BasicApplicationModel(BaseConfigModel):
  """Update Application Pydantic Request Model"""
  name: StrictStr
  description: StrictStr
  modules: list

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_APPLICATION_MODEL_EXAMPLE}


class FullApplicationDataModel(BasicApplicationModel):
  """Application Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class ApplicationModel(BasicApplicationModel):
  """Module Input Pydantic Model"""

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_APPLICATION_MODEL_EXAMPLE}


class PostApplicationResponseModel(BaseModel):
  """Module Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the application"
  data: FullApplicationDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the application",
            "data": FULL_APPLICATION_MODEL_EXAMPLE
        }
    }


class UpdateApplicationResponseModel(BaseModel):
  """Module Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the application"
  data: FullApplicationDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the application",
            "data": FULL_APPLICATION_MODEL_EXAMPLE
        }
    }


class GetApplicationResponseModel(BaseModel):
  """Module Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the application"
  data: FullApplicationDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the application",
            "data": FULL_APPLICATION_MODEL_EXAMPLE
        }
    }


class DeleteApplicationResponseModel(BaseModel):
  """Delete Module Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the application"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the application"
        }
    }


class AllApplicationResponseModel(BaseModel):
  """Module Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullApplicationDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_APPLICATION_MODEL_EXAMPLE]
        }
    }


class UpdateApplicationModel(BaseModel):
  """Update Module Pydantic Request Model"""
  name: Optional[StrictStr]
  description: Optional[StrictStr]
  modules: Optional[list]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_APPLICATION_MODEL_EXAMPLE}

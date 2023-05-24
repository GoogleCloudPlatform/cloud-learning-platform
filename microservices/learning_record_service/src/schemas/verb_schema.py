"""
Pydantic Models for Verb API's
"""
from typing import Optional, List
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_VERB_MODEL_EXAMPLE,
                                     FULL_VERB_MODEL_EXAMPLE)
# pylint: disable = line-too-long


class BasicVerbModel(BaseModel):
  """Verb Skeleton Pydantic Model"""
  name: str
  url: Optional[str] = ""
  canonical_data: Optional[dict] = {}


class FullVerbDataModel(BasicVerbModel):
  """Verb Skeleton Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class VerbModel(BasicVerbModel):
  """Verb Input Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_VERB_MODEL_EXAMPLE}


class UpdateVerbModel(BaseModel):
  """Update Verb Pydantic Model"""
  name: Optional[str]
  url: Optional[str]
  canonical_data: Optional[dict]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_VERB_MODEL_EXAMPLE}


class GetVerbResponseModel(BaseModel):
  """Verb Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the verb"
  data: Optional[FullVerbDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the verb",
            "data": FULL_VERB_MODEL_EXAMPLE
        }
    }


class PostVerbResponseModel(BaseModel):
  """Verb Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the verb"
  data: Optional[FullVerbDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the verb",
            "data": FULL_VERB_MODEL_EXAMPLE
        }
    }


class UpdateVerbResponseModel(BaseModel):
  """Verb Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the verb"
  data: Optional[FullVerbDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the verb",
            "data": FULL_VERB_MODEL_EXAMPLE
        }
    }


class DeleteVerb(BaseModel):
  """Delete Verb Pydantic Model"""
  success: bool = True
  message: str = "Successfully deleted the verb"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the verb"
        }
    }


class AllVerbsResponseModel(BaseModel):
  """Verb Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullVerbDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_VERB_MODEL_EXAMPLE]
        }
    }


class VerbImportJsonResponse(BaseModel):
  """Verb Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the verbs"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the verbs",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }

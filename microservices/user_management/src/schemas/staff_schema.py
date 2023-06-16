"""
Pydantic Model for Staff API's
"""
import json
import re
import regex
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, constr, Extra, validator
from schemas.schema_examples import (BASIC_STAFF_EXAMPLE, FULL_STAFF_EXAMPLE,
                                     PROFILE_FIELDS)

with open("./data/profile_fields.json", "r", encoding="utf-8") as f:
  fields = json.load(f)
  pronouns = fields["pronouns"]
  workdays = fields["workdays"]
  timezones = fields["timezones"]

PRONOUNS = Literal[tuple(pronouns)]
WORKDAYS = Literal[tuple(workdays)]
TIMEZONES = Literal[tuple(timezones)]


class AvailabilityModel(BaseModel):
  """Availability Pydantic Model"""
  day_of_week: List[WORKDAYS]
  start_time: str
  end_time: str


class BasicStaffModel(BaseModel):
  """Staff Skeleton Pydantic Model"""
  first_name: str
  last_name: str
  email: constr(
      min_length=7,
      max_length=128,
      regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
  preferred_name: Optional[str] = ""
  bio: Optional[str] = ""
  pronoun: Optional[PRONOUNS]
  phone_number: Optional[str] = ""
  shared_inboxes: Optional[str] = ""
  timezone: Optional[TIMEZONES]
  office_hours: Optional[List[AvailabilityModel]] = []
  photo_url: Optional[str] = ""

  # pylint: disable=no-self-argument
  @validator("preferred_name")
  def validate_preferred_name(cls, v):
    assert v == "" or re.match(r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]+$", v),\
      "Invalid format for preferred_name"
    return v
  @validator("first_name")
  def first_name_regex(cls,value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}]+$", value)
    if len(value)<=60 and result:
      return value
    raise ValueError("Invalid first name format")
  @validator("last_name")
  def last_name_regex(cls,value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", value)
    if len(value)<=60 and result:
      return value
    raise ValueError("Invalid last name format")

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_STAFF_EXAMPLE}


class FullStaffModel(BasicStaffModel):
  """Staff Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str


class StaffSearchResponseModel(BaseModel):
  """Staff Search Response Pydantic Model"""
  success: bool = True
  message: str = "Successfully fetched the Staffs"
  data: List[FullStaffModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the Staffs",
            "data": [FULL_STAFF_EXAMPLE]
        }
    }


class UpdateStaffModel(BaseModel):
  """Update Staff Pydantic Model"""
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  preferred_name: Optional[constr(
      max_length=60,
      regex=r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]+$")] = None
  bio: Optional[str] = ""
  pronoun: Optional[PRONOUNS]
  phone_number: Optional[str] = ""
  shared_inboxes: Optional[str] = ""
  timezone: Optional[TIMEZONES]
  office_hours: Optional[List[AvailabilityModel]] = []
  photo_url: Optional[str]
  email : Optional[constr(
      min_length=7,
      max_length=128,
      regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")]

  # pylint: disable=no-self-argument
  @validator("first_name")
  def first_name_regex(cls,value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}]+$", value)
    if len(value)<=60 and result:
      return value
    raise ValueError("Invalid first name format")
  @validator("last_name")
  def last_name_regex(cls,value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", value)
    if len(value)<=60 and result:
      return value
    raise ValueError("Invalid last name format")
  class Config:
    extra = Extra.forbid


class GetStaffResponseModel(BaseModel):
  """Get Staff Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the Staff"
  data: Optional[FullStaffModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the Staff",
            "data": FULL_STAFF_EXAMPLE
        }
    }


class PostStaffResponseModel(BaseModel):
  """Create Staff Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the Staff"
  data: FullStaffModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the Staff",
            "data": FULL_STAFF_EXAMPLE
        }
    }


class UpdateStaffResponseModel(BaseModel):
  """Update Staff Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the Staff"
  data: Optional[FullStaffModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the Staff",
            "data": FULL_STAFF_EXAMPLE
        }
    }


class DeleteStaffReponseModel(BaseModel):
  """Delete Staff Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the Staff"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the Staff"
        }
    }


class AllStaffResponseModel(BaseModel):
  """Get All Staff Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Data fetched successfully"
  data: Optional[List[FullStaffModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Data fetched successfully",
            "data": [FULL_STAFF_EXAMPLE]
        }
    }


class StaffImportJsonResponse(BaseModel):
  """Staff Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the Staffs"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the Staffs",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class ProfileFieldsModel(BaseModel):
  pronouns: Optional[list]
  workdays: Optional[list]
  timezones: Optional[list]


class ProfileFieldsResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the possible options for"\
                            " pronouns, workdays, timezones"
  data: Optional[ProfileFieldsModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the possible options for"
                    " pronouns, workdays, timezones",
        "data": PROFILE_FIELDS
      }
    }

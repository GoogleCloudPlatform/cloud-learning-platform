"""
Pydantic Model for Learner API"s
"""
import regex
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, constr, validator
from schemas.schema_examples import (
  BASIC_LEARNER_EXAMPLE,
  FULL_LEARNER_EXAMPLE,
  UPDATE_LEARNER_EXAMPLE
)


class BasePhoneNumber(BaseModel):
  """Base Phone number Pydandic Model"""
  phone_number_type: Optional[Literal["Home", "Work", "Mobile", "Fax",
  "Other"]] = "Work"
  primary_phone_number_indicator: Optional[Literal["Yes", "No"]] = "Yes"
  phone_number: Optional[constr(max_length=24)] = ""
  phone_do_not_publish_indicator: Optional[Literal["Yes", "No",
  "Unknown"]] = "Yes"
  phone_number_listed_status: Optional[Literal["Listed", "Unlisted",
  "Unknown"]] = "Listed"


class PhoneNumber(BaseModel):
  """Phone Number Pydantic Model"""
  mobile: Optional[BasePhoneNumber] = {}
  telephone: Optional[BasePhoneNumber] = {}


class BasicLearnerModel(BaseModel):
  """Learner Skeleton Pydantic Model"""
  first_name: str
  middle_name: Optional[constr(
    max_length=60,
    regex=r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]*$")] = ""
  last_name: str
  suffix: Optional[constr(max_length=10, regex="^[a-zA-Z0-9]*$")] = ""
  prefix: Optional[constr(max_length=30, regex="^[a-zA-Z0-9]*$")] = ""

  preferred_name: Optional[constr(max_length=100, regex="^[a-zA-Z0-9]*$")] = ""
  preferred_first_name: Optional[constr(max_length=100,
                                        regex="^[a-zA-Z0-9]*$")] = ""
  preferred_middle_name: Optional[constr(max_length=100,
                                         regex="^[a-zA-Z0-9]*$")] = ""
  preferred_last_name: Optional[constr(max_length=100,
                                       regex="^[a-zA-Z0-9]*$")] = ""
  preferred_name_type: Optional[Literal["Alias", "NickName", "PreferredName",
  "PreviousLegalName",
  "PreferredFamilyName",
  "PreferredGivenName",
  "FullName"]] = "PreferredName"
  preferred_pronoun: Optional[str] = ""

  student_identifier: Optional[constr(max_length=40)] = ""
  student_identification_system: Optional[constr(max_length=15)] = ""
  personal_information_verification: Optional[str] = ""
  personal_information_type: Optional[str] = ""

  address_type: Optional[constr(max_length=30)] = ""
  street_number_and_name: Optional[constr(max_length=100)] = ""
  apartment_room_or_suite_number: Optional[constr(max_length=100)] = ""
  city: Optional[constr(max_length=100)] = ""
  state_abbreviation: Optional[constr(max_length=2)] = ""
  postal_code: Optional[constr(max_length=17)] = ""
  country_name: Optional[constr(max_length=30)] = ""
  country_code: Optional[constr(max_length=2)] = ""
  latitude: Optional[constr(max_length=20)] = ""
  longitude: Optional[constr(max_length=20)] = ""
  country_ansi_code: Optional[int] = 10000
  address_do_not_publish_indicator: Optional[Literal["Yes", "No",
  "Unknown"]] = "Yes"
  phone_number: Optional[PhoneNumber] = {}
  email_address_type: Optional[Literal["Home", "Work", "Organizational",
  "Other"]] = "Work"
  email_address: constr(
    min_length=7,
    max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
  email_do_not_publish_indicator: Optional[Literal["Yes", "No",
  "Unknown"]] = "Yes"
  backup_email_address: Optional[str] = ""

  birth_date: Optional[str]
  gender: Optional[Literal["Male", "Female", "NotSelected"]] = "NotSelected"
  country_of_birth_code: Optional[str]
  ethnicity: Optional[constr(max_length=100)]

  organisation_email_id: Optional[constr(
    min_length=7,
    max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")] = (
    "test@mail.com")
  employer_id: Optional[str] = ""
  affiliation: Optional[str] = ""
  employer: Optional[str] = ""
  employer_email: Optional[constr(
    min_length=7,
    max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")] = (
    "test@mail.com")

  # pylint: disable=no-self-argument
  @validator("first_name")
  def name_regex(cls, value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", value)
    if len(value) <= 60 and result:
      return value
    raise ValueError("Invalid first format")

  @validator("last_name")
  def last_name_regex(cls, value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", value)
    if len(value) <= 60 and result:
      return value
    raise ValueError("Invalid last name format")


class FullLearnerDataModel(BasicLearnerModel):
  """Learner Skeleton Model with uuid, created and updated time"""
  uuid: str
  is_archived: bool
  created_time: str
  last_modified_time: str


class LearnerModel(BasicLearnerModel):
  """Learner Pydantic Model"""

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_LEARNER_EXAMPLE}


class UpdateLearnerModel(BaseModel):
  """Update Learner Pydantic Model"""
  first_name: Optional[str]
  last_name: Optional[str]
  preferred_name: Optional[constr(max_length=100, regex="^[a-zA-Z0-9]*$")]
  preferred_first_name: Optional[constr(max_length=100, regex="^[a-zA-Z0-9]*$")]
  preferred_middle_name: Optional[constr(
    max_length=100, regex="^[a-zA-Z0-9]*$")]
  preferred_last_name: Optional[constr(max_length=100, regex="^[a-zA-Z0-9]*$")]

  preferred_name_type: Optional[Literal["Alias", "NickName", "PreferredName",
  "PreviousLegalName",
  "PreferredFamilyName",
  "PreferredGivenName", "FullName"]]
  preferred_pronoun: Optional[str]
  student_identifier: Optional[constr(max_length=40)]
  student_identification_system: Optional[constr(max_length=15)]
  personal_information_verification: Optional[str]
  personal_information_type: Optional[str]

  address_type: Optional[constr(max_length=30)]
  street_number_and_name: Optional[constr(max_length=100)]
  apartment_room_or_suite_number: Optional[constr(max_length=100)]
  city: Optional[constr(max_length=100)]
  state_abbreviation: Optional[constr(max_length=2)]
  postal_code: Optional[constr(max_length=17)]
  country_name: Optional[constr(max_length=30)]
  country_code: Optional[constr(max_length=2)]
  latitude: Optional[constr(max_length=20)]
  longitude: Optional[constr(max_length=20)]
  country_ansi_code: Optional[int]
  address_do_not_publish_indicator: Optional[Literal["Yes", "No", "Unknown"]]

  phone_number: Optional[PhoneNumber]
  email_address_type: Optional[Literal["Home", "Work", "Organizational",
  "Other"]]
  email_address: Optional[constr(
    min_length=7,
    max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")]
  email_do_not_publish_indicator: Optional[Literal["Yes", "No", "Unknown"]]
  backup_email_address: Optional[str]

  birth_date: Optional[str]
  gender: Optional[Literal["Male", "Female", "NotSelected"]]
  country_of_birth_code: Optional[str]
  ethnicity: Optional[constr(max_length=100)]

  organisation_email_id: Optional[constr(
    min_length=7,
    max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")]
  employer_id: Optional[str]
  affiliation: Optional[str]
  is_archived: Optional[bool]
  employer: Optional[str]
  employer_email: Optional[constr(
    min_length=7,
    max_length=128,
    regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")]

  # pylint: disable=no-self-argument
  @validator("first_name")
  def name_regex(cls, value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", value)
    if len(value) <= 60 and result:
      return value
    raise ValueError("Invalid first format")

  @validator("last_name")
  def last_name_regex(cls, value):
    result = regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", value)
    if len(value) <= 60 and result:
      return value
    raise ValueError("Invalid last name format")

  class Config():
    orm_mode = True
    extra = "forbid"
    schema_extra = {"example": UPDATE_LEARNER_EXAMPLE}


class GetLearnerResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learner"
  data: Optional[FullLearnerDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learner",
        "data": FULL_LEARNER_EXAMPLE
      }
    }


class PostLearnerResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learner"
  data: Optional[FullLearnerDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the learner",
        "data": FULL_LEARNER_EXAMPLE
      }
    }


class UpdateLearnerResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the learner"
  data: FullLearnerDataModel

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully updated the learner",
        "data": FULL_LEARNER_EXAMPLE
      }
    }


class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullLearnerDataModel]]
  total_count: int


class AllLearnersResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learners"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learners",
        "data": {
          "records": [FULL_LEARNER_EXAMPLE],
          "total_count": 50
        }
      }
    }


class DeleteLearner(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the learner"

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully deleted the learner"
      }
    }


class LearnerSearchResponseModel(BaseModel):
  """Learner Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learners"
  data: Optional[List[FullLearnerDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learners",
        "data": [FULL_LEARNER_EXAMPLE]
      }
    }


class LearnerImportJsonResponse(BaseModel):
  """Learner Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learners"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the learners",
        "data": [
          "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
          "lQRzcrRuDpJ9IoW8bCHu"
        ]
      }
    }


class LearnerPathwayId(BaseModel):
  curriculum_pathway_id: str = ""


class GetLearnerPathwayIdResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetch the curriculum " \
                           "pathway for the learner"
  data: Optional[LearnerPathwayId]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetch the curriculum "
                   "pathway id for the learner",
        "data": {
          "curriculum_pathway_id": "44qxEpc35pVMb6AkZGbi"
        }
      }
    }


class InstructorModel(BaseModel):
  """Instructor Detail Pydantic Model"""
  instructor_staff_id: str = ""
  instructor_user_id: str = ""


class InstructorResponseModel(BaseModel):
  """Instructor Details Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched instructor details"
  data: Optional[InstructorModel] = {}

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched instructor details",
        "data": {
          "instructor_staff_id": "44qxEpc35pVMb6AkZGbi",
          "instructor_user_id": "00MPqUhCbyPe1BcevQDr"
        }
      }
    }


class CoachIdResponse(BaseModel):
  coach_staff_id: str = ""
  coach_user_id: str = ""


class CoachesResponseModel(BaseModel):
  """Get Coaches Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the coach"
  data: Optional[CoachIdResponse] = {}

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the coach",
        "data": {
          "coach_staff_id": "44qxEpc35pVMb6AkZGbi",
          "coach_user_id": "lQRzcrRuDpJ9IoW8bCHu"
        }
      }
    }


class GetInstructorsModel(BaseModel):
  """Instructor Detail Pydantic Model"""
  user_id: str
  staff_id: str
  discipline_id: str
  discipline_name: str


class GetInstructorsResponseModel(BaseModel):
  """Instructor Details Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched instructor details"
  data: Optional[List[GetInstructorsModel]] = []

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched instructor details",
        "data": [
          {
            "instructor_id": "44qxEpc35pVMb6AkZGbi",
            "staff_id": "Qh49RVbvHRIRAFx304YL",
            "discipline_id": "gMXvlgMXoNQCRUKuXxLC",
            "discipline_name": "Humanities"
          }
        ]
      }
    }

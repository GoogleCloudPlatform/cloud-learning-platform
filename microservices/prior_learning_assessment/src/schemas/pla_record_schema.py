"""
Pydantic Model for PLA Record API's
"""
from typing import List, Optional, Union
from pydantic import BaseModel
from schemas.schema_examples import (BASIC_PLA_RECORD_MODEL_EXAMPLE,
                                     FULL_PLA_RECORD_MODEL_EXAMPLE,
                                     UPDATE_PLA_RECORD_MODEL_EXAMPLE)
from config import STATUS_PLA_RECORD,RECORD_TYPE


class BasicPLARecordModel(BaseModel):
  """PLA Record Skeleton Pydantic Model"""
  title: Optional[str]
  user_id: str
  type: Optional[RECORD_TYPE] = "draft"
  assessor_name: str
  description: Optional[str]
  status: Optional[STATUS_PLA_RECORD] = "In progress"
  progress: Optional[int]
  prior_experiences: Optional[List[Union[str, dict]]]
  approved_experiences: Optional[List[Union[str, dict]]]


class FullPLARecordDataModel(BasicPLARecordModel):
  """PLA Record Skeleton Model with uuid, created and updated time"""
  id_number: int
  progress: int
  is_archived: bool
  is_flagged: bool
  uuid: str
  created_time: str
  last_modified_time: str

  class Config():
    orm_mode = True
    schema_extra = {"example": FULL_PLA_RECORD_MODEL_EXAMPLE}

class PLARecordModel(BasicPLARecordModel):
  """PLA Record Pydantic Model"""
  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_PLA_RECORD_MODEL_EXAMPLE}
    extra = "forbid"

class UpdatePLARecordModel(BasicPLARecordModel):
  """Update PLA Record Skeleton Model"""
  user_id: Optional[str]
  type: Optional[str]
  assessor_name: Optional[str]
  status: Optional[str]
  id_number: Optional[int]
  is_archived: Optional[bool]
  is_flagged: Optional[bool]


  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_PLA_RECORD_MODEL_EXAMPLE}
    extra = "forbid"


class UpdatePLARecordExperienceModel(BaseModel):
  """Update PLA Record Model to append or remove experiences from PLA Record"""
  prior_experiences: Optional[List[str]]
  approved_experiences: Optional[List[str]]


class GetPLARecordModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the PLA Record"
  data: FullPLARecordDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the PLA Record",
            "data": FULL_PLA_RECORD_MODEL_EXAMPLE
        }
    }


class PLAReportExperiencesModel(BaseModel):
  experiences_with_matches: Optional[List] = []
  experiences_without_matches: Optional[List] = []


class PLAReportResponseModel(FullPLARecordDataModel):
  experiences_found: int
  experiences_matched: int
  potential_credits: int
  experiences: PLAReportExperiencesModel


class GetPLAReportResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully generated the PLA Record report"
  data: PLAReportResponseModel


class PostPLARecordModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the PLA Record"
  data: FullPLARecordDataModel


  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the PLA Record",
            "data": FULL_PLA_RECORD_MODEL_EXAMPLE
        }
    }


class UpdatePLARecordModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the PLA Record"
  data: FullPLARecordDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the PLA Record ",
            "data": FULL_PLA_RECORD_MODEL_EXAMPLE
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullPLARecordDataModel]]
  total_count: int

class AllPLARecordModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the PLA Records"
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the PLA records",
            "data": {
                      "records":[FULL_PLA_RECORD_MODEL_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class DeletePLARecordModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the PLA Record"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the PLA Record"
        }
    }


class PLARecordSearchModelResponse(BaseModel):
  """PLA Record Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the PLA Records"
  data: TotalCountResponseModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the PLA Records",
            "data": {
              "records":[FULL_PLA_RECORD_MODEL_EXAMPLE],
              "total_count": 50
              }
        }
    }

class PLARecordImportJsonResponse(BaseModel):
  """PLA Record Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the pla_records"
  data: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success":
                True,
            "message":
                "Successfully created the pla_records",
            "data": [
                "abscde1234", "00mmpeodma",
                "jklmu12345"
            ]
        }
    }


class AllAssessorsResponseModel(BaseModel):
  """ApprovedOgranisations Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = \
    "Successfully fetched the unique list of Assessor names"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": \
              "Successfully fetched the unique list of Assessor names",
            "data": ["name1", "name2", "name3", "name4"]
        }
    }

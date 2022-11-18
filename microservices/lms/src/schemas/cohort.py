"""
Pydantic Model for cohort API's
"""
import datetime
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import COHORT_EXAMPLE,INSERT_COHORT_EXAMPLE

class CohortModel(BaseModel):
    uuid: str
    name: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    registration_start_date: datetime.datetime
    registration_end_date: datetime.datetime
    max_student: Optional[int]=0
    enrolled_student_count:Optional[int]=0
    course_template: str 

    class Config():
        orm_mode = True
        schema_extra = {
            "example": COHORT_EXAMPLE
        }


class CohortListModel(BaseModel):
    success: Optional[bool] = True
    message: Optional[str] = "Successfully get the Cohort list"
    cohort_list: Optional[list[CohortModel]]

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully get the Cohort list",
                "cohort_list": [COHORT_EXAMPLE]
            }
        }


class CreateCohortResponseModel(BaseModel):
    success: Optional[bool] = True
    message: Optional[str] = "Successfully created the cohort"
    cohort: Optional[CohortModel]

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully created the cohort",
                "cohort": COHORT_EXAMPLE
            }}


class InputCohort(BaseModel):
    name: str
    description: str
    start_date: datetime.datetime
    end_date:datetime.datetime
    registration_start_date:datetime.datetime
    registration_end_date:datetime.datetime
    max_student:int
    course_template_uuid:str
    class Config():
        orm_mode = True
        schema_extra = {
            "example": INSERT_COHORT_EXAMPLE
        }


class DeleteCohort(BaseModel):
  """Delete cohort Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the cohort"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the cohort",
            "data": None
        }
    }

"""
Pydantic Model for cohort API's
"""
import datetime
from typing import Optional
from pydantic import BaseModel
from schemas.schema_examples import COHORT_EXAMPLE, INSERT_COHORT_EXAMPLE,UPDATE_COHORT_EXAMPLE


class CohortModel(BaseModel):
  """Cohort Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  uuid: str
  name: str
  description: str
  start_date: datetime.datetime
  end_date: datetime.datetime
  registration_start_date: datetime.datetime
  registration_end_date: datetime.datetime
  max_students: Optional[int] = 0
  enrolled_students_count: Optional[int] = 0
  course_template: str

  class Config():
    "Pydantic Config Class"
    orm_mode = True
    schema_extra = {"example": COHORT_EXAMPLE}


class UpdateCohortModel(BaseModel):
  """Update Cohort Pydantic Model

  Args:
      BaseModel (_type_): _description_
  """
  name: Optional[str] = None
  description: Optional[str] = None
  start_date: Optional[datetime.datetime] = None
  end_date: Optional[datetime.datetime] = None
  registration_start_date: Optional[datetime.datetime] = None
  registration_end_date: Optional[datetime.datetime] = None
  max_students: Optional[int] = None
  enrolled_students_count: Optional[int] = None
  course_template: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {"example": UPDATE_COHORT_EXAMPLE}


class CohortListResponseModel(BaseModel):
  """Cohort List Response model"""
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
  """Create Cohort Response Model"""
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
        }
    }


class InputCohortModel(BaseModel):
  """Pydantic Input Cohort Model

  Args:
      BaseModel (_type_): _description_
  """
  name: str
  description: str
  start_date: datetime.datetime
  end_date: datetime.datetime
  registration_start_date: datetime.datetime
  registration_end_date: datetime.datetime
  max_students: int
  course_template_uuid: str

  class Config():
    orm_mode = True
    schema_extra = {"example": INSERT_COHORT_EXAMPLE}


class UpdateCohortResponseModel(BaseModel):
  """Update cohort response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Updated the cohort"
  cohort: Optional[CohortModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Updated the cohort",
            "cohort": COHORT_EXAMPLE
        }
    }


class DeleteCohortResponseModel(BaseModel):
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

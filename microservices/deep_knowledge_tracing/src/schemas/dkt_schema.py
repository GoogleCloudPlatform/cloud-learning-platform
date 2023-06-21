"""
  Pydantic schemas for DKT API's
"""
from typing import Optional,Dict,List
from pydantic import BaseModel
from typing_extensions import Literal



class CreateDataDKTRequest(BaseModel):
  num_users: int
  num_lus: int
  item_type: Optional[str] = "ctf"

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "num_users": 50,
            "num_lus": 10,
            "item_type": "ctf"
        }
    }

class CreateDataDKTResponse(BaseModel):
  success: bool
  message: str

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the fake data"
        }
    }

class Data(BaseModel):
  experiment_id: Optional[str]
  status: Optional[str]

class TrainDKTRequest(BaseModel):
  course_id: Optional[str]
  title: Optional[str]

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "course_id": "sample_course_id",
            "title": "sample_title_to_track_training"
        }
    }

class TrainDKTResponse(BaseModel):
  success: bool
  message: str
  data: Optional[Data]

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully initiated the job with type\
            'deep-knowledge-tracing'.\
            Please use the job name to track the job status",
            "data": {
                "experiment_id": "abcd-ajdf-sdfk-sdff",
                "status": "active"
            }
        }
    }

class PredictDKTRequest(BaseModel):
  course_id: str
  user_id: str
  session_id: str

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "course_id": "sample_course_id",
            "user_id": "sample_user_id",
            "session_id": "sample_session_id"
        }
    }

class PredictDKTResponse(BaseModel):
  success: bool
  message: str
  data: Dict[str,float]

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully generated predictions from dkt model",
            "data": {"sample_lu_id":0.91}
        }
    }

class UserEventModel(BaseModel):
  learning_unit : str
  is_correct : Literal[0, 1]

class InferenceDKTRequest(BaseModel):
  course_id: str
  user_id: str
  user_events : List[dict]

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "course_id": "sample_course_id",
            "user_id": "sample_user_id",
            "user_events": [{"learning_unit": "sample_lu_id", "is_correct": 0}]
        }
    }

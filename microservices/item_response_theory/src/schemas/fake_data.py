"""Schema for creating fake data"""

from typing import Optional
from pydantic import BaseModel

class FakeIRTDataRequest(BaseModel):
  num_users: int
  num_items: int
  item_type: Optional[str] = "ctf"

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "num_users": 50,
            "num_items": 50,
            "item_type": "ctf"
        }
    }

class CourseFakeIRTDataRequest(BaseModel):
  num_users: int
  course_id: str

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "num_users": 10,
            "course_id":"sdfjaskfdla"
        }
    }

class FakeDataResponse(BaseModel):
  success: bool
  message: str
  data: dict

  class Config:
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the fake data",
            "data": {
                "learning_unit_id": "dfasfhakjs"
            }
        }
    }

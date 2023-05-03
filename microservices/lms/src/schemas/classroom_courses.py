"""
Pydantic Model for copy course API's
"""
from pydantic import BaseModel
from typing import  Optional
from schemas.schema_examples import COURSE_EXAMPLE


class CourseDetails(BaseModel):
  """Course Detail model"""
  course_id: str

class EnableNotificationsResponse(BaseModel):
  """Enable Notifications API Response Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully registered the course"
  data: Optional[list[dict]] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully registered the course",
            "data": []
        }
    }

class CopyCourseResponse(BaseModel):
  """Copy Course Response Model"""
  success: Optional[bool] = True
  message: Optional[str]="Successfully Copied the course"
  data: Optional[dict]=None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully Copied the course",
            "data": {"new_course":{},
                    "coursework_list":[],
                    "coursework_material":[]}
        }
    }

class ClassroomModel(BaseModel):
  """Classroom Course pydantic model"""
  id: str
  name: Optional[str]
  section: Optional[str]
  description_heading: Optional[str]
  description: Optional[str]
  room: Optional[str]
  owner_id: Optional[str]
  creation_time: Optional[str]
  update_time: Optional[str]
  enrollment_code: Optional[str]
  course_state: Optional[str]
  alternate_link: Optional[str]
  teacher_group_email: Optional[str]
  course_group_email: Optional[str]
  teacher_folder: Optional[dict]
  course_material_sets: Optional[list[dict]]
  guardians_enabled: bool
  calendar_id: Optional[str]
  gradebook_settings: Optional[dict]

class ClassroomResponseModel(BaseModel):
  """Classroom course response pydantic model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetch course by this id"
  data: Optional[ClassroomModel]
  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Success",
            "data": COURSE_EXAMPLE
        }
    }


class ClassroomCourseListResponseModel(BaseModel):
  """Get a list of Classroom Courses"""
  success: Optional[bool] = True
  message: Optional[str] = "Success list"
  data: Optional[list[ClassroomModel]] = []

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Success",
            "data": [COURSE_EXAMPLE]
        }
    }

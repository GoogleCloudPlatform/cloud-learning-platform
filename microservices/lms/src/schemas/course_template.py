"""
Pydantic Model for Course template API's
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

COURSE_TEMPLATE_EXAMPLE = {
    "uuid": "id",
    "name": "name",
    "description": "description",
    "admin": "admin",
    "instructional_designer": "IDesiner",
    "classroom_id": "clID",
    "classroom_code": "clcode"
}
INSERT_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
    "admin": "admin",
    "instructional_designer": "IDesiner"
}


class CourseTemplateModel(BaseModel):
    uuid: str
    name: str
    description: str
    admin: str
    instructional_designer: str
    classroom_id: Optional[str]
    classroom_code: Optional[str]

    class Config():
        orm_mode = True
        schema_extra = {
            "example": COURSE_TEMPLATE_EXAMPLE
        }


class CourseTemplateListModel(BaseModel):
    success: Optional[bool] = True
    message: Optional[str] = "Successfully get the course template list"
    course_template_list: Optional[list[CourseTemplateModel]]

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully get the course template list",
                "course_template_list": [COURSE_TEMPLATE_EXAMPLE]
            }
        }


class CreateCourseTemplateResponseModel(BaseModel):
    success: Optional[bool] = True
    message: Optional[str] = "Successfully created the course template"
    course_template: Optional[CourseTemplateModel]

    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully created the course template",
                "course_template": COURSE_TEMPLATE_EXAMPLE
            }}


class InputCourseTemplateModel(BaseModel):
    name: str
    description: str
    admin: str
    instructional_designer: str

    class Config():
        orm_mode = True
        schema_extra = {
            "example": INSERT_COURSE_TEMPLATE_EXAMPLE
        }


class DeleteCourseTemplateModel(BaseModel):
  """Delete Course Template Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the course template"
  data: Optional[str] = None

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the course template",
            "data": None
        }
    }

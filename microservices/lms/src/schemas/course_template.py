"""
Pydantic Model for Course template API's
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

COURSE_TEMPLATE_EXAMPLE={
            "id":"id",
            "course_name" : "name",
            "course_description" : "description",
            "course_topic" :"topic",
            "course_admin" : "admin",
            "course_instructional_designer": "IDesiner",
            "course_classroom_id":"clID",
            "course_classroom_code":"clcode"   
        }
INSERT_COURSE_TEMPLATE_EXAMPLE={
    "course_name" : "name",
    "course_description" : "description",
    "course_topic" :"topic",
    "course_admin" : "admin",
    "course_instructional_designer": "IDesiner"
}
class CourseTemplateModel(BaseModel):
    uuid:str
    name : str
    description : str
    topic :str
    admin : str
    instructional_designer: str
    classroom_id:Optional[str]
    classroom_code:Optional[str]


    class Config():
        orm_mode = True
        schema_extra = {
            "example": COURSE_TEMPLATE_EXAMPLE
        }
class CourseTemplateListModel(BaseModel):
    message: Optional[str] = "Successfully get the course list"
    course_template_list: Optional[list[CourseTemplateModel]]
    class Config():
        orm_mode = True
        schema_extra = {
            "example": {
            "message":"Successfully get the course list",
            "course_template_list":[COURSE_TEMPLATE_EXAMPLE]
        }
        }
class CreateCourseTemplateResponseModel(BaseModel):
    message:Optional[str]="Successfully created the course template"
    course_template:Optional[CourseTemplateModel]

    class Config():
        orm_mode= True
        schema_extra={
            "example":{
                "message":"Successfully created the course template",
                "course_template":COURSE_TEMPLATE_EXAMPLE
            }}

class InputCourseTemplateModel(BaseModel):
    course_name:str
    course_description:str
    course_topic:str
    course_admin:str
    course_instructional_designer:str

    class Config():
        orm_mode=True
        schema_extra={
            "example":INSERT_COURSE_TEMPLATE_EXAMPLE
        }



    
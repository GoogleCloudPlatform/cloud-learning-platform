"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel

class SectionDetails(BaseModel):
    """Course Detail model"""
    name:str
    description:str
    course_template:str
    cohort:str
    teachers_list:list


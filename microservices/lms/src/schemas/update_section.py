"""
Pydantic Model for copy course API's
"""
from typing import Optional
from pydantic import BaseModel

class update_section(BaseModel):
    """Course Detail model"""
    course_id:str
    section_name:str
    description:str
    course_state:str

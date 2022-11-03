"""
Pydantic Model for copy course API's
"""
# from turtle import st
from typing import Optional
from pydantic import BaseModel

class CourseDetails(BaseModel):
    """Course Detail model"""
    course_id:str



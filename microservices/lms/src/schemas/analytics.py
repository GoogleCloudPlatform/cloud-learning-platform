"""
Pydantic Model for copy course API's
"""
import datetime
import json
from pydantic import BaseModel, validator
from common.utils.logging_handler import Logger
from typing import  Optional
from schemas.schema_examples import (
  ANALYTICS_USER_EXAMPLE,ANALYTICS_COURSE_EXAMPLE,ANALYTICS_COURSE_WORK_EXAMPLE
  )


def convert_str_array_to_dict_array(list_obj):
  """convery list of string to list of dict if required

  Args:
      list_obj (list[str]): list of json strings

  Returns:
      list[dict]: list of dict
  """
  if not list_obj:
    return []
  if isinstance(list_obj[0],dict):
    return list_obj
  dict_list=[]
  for i in list_obj:
    dict_list.append(json.loads(i))
  return dict_list

def convert_str_to_dict(obj):
  """convert obj to dict if required

  Args:
      obj (str): json string

  Returns:
      dict: return dict
  """
  if not obj:
    return None
  if isinstance(obj,dict):
    return obj
  return json.loads(obj)

class AnalyticsUser(BaseModel):
  """User Pydantic Model for Analytics Response"""
  user_id: Optional[str]=""
  user_gaia_id: str
  user_name: dict
  user_email_address: str
  user_photo_url: str
  user_permissions: list[dict]
  user_verified_teacher: Optional[bool]=None

  @validator("user_permissions",pre=True)
  @classmethod
  def user_list_dict_validator(cls,v):
    """User Permission validator for list of dict"""
    return convert_str_array_to_dict_array(v)
  class Config():
    orm_mode = True
    schema_extra = {
      "example":ANALYTICS_USER_EXAMPLE
    }

class AnalyticsCourseWork(BaseModel):
  """Course Work Pydantic Model for Analytics Response"""
  course_work_id : Optional[str]=""
  course_work_title : Optional[str]=""
  course_work_description : Optional[str]=""
  course_work_materials: Optional[list[dict]]=[]
  course_work_state: Optional[str]=""
  course_work_alternate_link: Optional[str]=""
  course_work_creation_time: Optional[datetime.datetime]=None
  course_work_update_time: Optional[datetime.datetime]=None
  course_work_due_date: Optional[datetime.date]={}
  course_work_due_time: Optional[datetime.time]={}
  course_work_schedule_time: Optional[str]=""
  course_work_max_points: Optional[int]=0
  course_work_work_type: Optional[str]=""
  course_work_associated_with_developer: Optional[bool]=None
  course_work_assignee_mode: Optional[str]=""
  course_work_individual_students_options: Optional[dict]={}
  course_work_submission_modification_mode: Optional[str]=""
  course_work_creator_user_id: Optional[str]=""
  course_work_topic_id: Optional[str]=""
  course_work_grade_category: Optional[dict]={}
  course_work_assignment: Optional[dict]={}
  course_work_multiple_choice_question: Optional[dict]={}
  submission_id: Optional[str]=None
  submission_assigned_grade: Optional[int]=0
  submission_creation_time: Optional[datetime.datetime]=None
  submission_update_time: Optional[datetime.datetime]=None
  submission_late: Optional[bool]=None

  class Config():
    orm_mode = True
    schema_extra = {
      "example":ANALYTICS_COURSE_WORK_EXAMPLE
      }

  @validator("course_work_individual_students_options",
             "course_work_grade_category",
             "course_work_assignment",
             "course_work_multiple_choice_question",pre=True)
  @classmethod
  def dict_validator(cls, v):
    return convert_str_to_dict(v)

  @validator("course_work_materials",pre=True)
  @classmethod
  def list_dict_validator(cls,v):
    return convert_str_array_to_dict_array(v)

  @validator("course_work_due_date",pre=True)
  @classmethod
  def dict_to_datetime_date(cls,v):
    if not v:
      return None
    if isinstance(v,str):
      return datetime.date.fromisoformat(v)
    if isinstance(v,datetime.date):
      return v
    return datetime.date(
        year=v["year"],
        month=v["month"],
        day=v["day"])

  @validator("course_work_due_time",pre=True)
  @classmethod
  def dict_to_datetime_time(cls,v):
    if not v:
      return None
    if isinstance(v,str):
      return datetime.time().fromisoformat(v)
    if isinstance(v,datetime.time):
      return v
    if v.get("minutes") is None:
      v["minutes"] = 0
    if v.get("hours") is None:
      v["hours"] = 0
    return datetime.time(
        hour=v["hours"],
        minute=v["minutes"])

class AnalyticsCourse(BaseModel):
  """User Pydantic Model for Analytics Response"""
  course_id: str
  course_name : str
  course_section : str
  course_description : str
  course_url : str
  section_id : str
  section_name :  str
  cohort_id :  str
  cohort_name :  str
  cohort_description :  str
  cohort_registration_start_date :  datetime.datetime
  cohort_registration_end_date :  datetime.datetime
  cohort_start_date :  datetime.datetime
  cohort_end_date :  datetime.datetime
  cohort_max_students :  int
  course_work_list: Optional[list[AnalyticsCourseWork]]=[]
  class Config():
    orm_mode = True
    schema_extra = {
      "example": ANALYTICS_COURSE_EXAMPLE
    }

class AnalyticsResponse(BaseModel):
  """Analytics API Response Pydantic model"""
  user: AnalyticsUser
  section_list: list[AnalyticsCourse]
  class Config():
    orm_mode = True
    schema_extra = {
      "example":{
        "user":ANALYTICS_USER_EXAMPLE,
        "section_list":[ANALYTICS_COURSE_EXAMPLE]
      }
    }

""" Helper Functions"""
import datetime
from fastapi import Depends
from common.utils.auth_service import validate_user_type_and_token, auth_scheme
from common.utils.errors import ResourceNotFoundException
from schemas.analytics import (
  AnalyticsCourse,AnalyticsCourseWork,
  AnalyticsSubmission,AnalyticsUser,AnalyticsResponse)

FEED_TYPES = ("COURSE_WORK_CHANGES", "COURSE_ROSTER_CHANGES")
def convert_cohort_to_cohort_model(cohort):
  """Convert Cohort Object to Cohort Model Object

  Args:
    cohort (Cohort): Cohort Object.
  Returns:
    return a dict in the cohort model format.
  """ ""
  loaded_cohort = cohort.to_dict()
  course_template = loaded_cohort.pop("course_template").to_dict()
  loaded_cohort["course_template"] = course_template["key"]
  loaded_cohort["course_template_name"] = course_template["name"]
  return loaded_cohort


def convert_section_to_section_model(section):
  """Convert Section Object to Section Model Object

  Args:
    section (Section): Section Object.
  Returns:
    return a dict in the section model format.
  """ ""
  loaded_section = section.to_dict()
  course_template = loaded_section.pop("course_template").to_dict()
  loaded_section["course_template"] = course_template["key"]
  cohort = loaded_section.pop("cohort").to_dict()
  loaded_section["cohort"] = cohort["key"]
  return loaded_section


def validate_user(token: auth_scheme = Depends()):
  return validate_user_type_and_token(["other", "faculty","admin"], token)


def convert_assignment_to_assignment_model(assignment):
  """Convert assignment dict to assignment object
  Args:
      assignment (dict): dict which contains all the assignment details
  Returns:
      dict: dict which contains assignment details
       according to assignment object
  """
  keys = assignment.keys()
  assignment["classroom_id"] = assignment["courseId"]
  assignment["creation_time"] = assignment["creationTime"]
  assignment["update_time"] = assignment["updateTime"]
  if "dueDate" in keys:
    assignment["due_date"] = datetime.date(
        year=assignment["dueDate"]["year"],
        month=assignment["dueDate"]["month"],
        day=assignment["dueDate"]["day"])
  if "dueTime" in keys:
    assignment["due_time"] = datetime.time(
        hour=assignment["dueTime"]["hours"],
        minute=assignment["dueTime"]["minutes"])
  assignment["link"] = get_json_value(assignment, "alternateLink")
  assignment["max_grade"] = get_json_value(assignment, "maxPoints")
  assignment["work_type"] = get_json_value(assignment, "workType")
  assignment["assignee_mode"] = get_json_value(assignment, "assigneeMode")
  return assignment


def get_json_value(dict_object, key):
  """check key in the dict and return value according it
  Args:
    dict_object (dict): dict
    key (str): _description_
  Returns:
    _type_: _description_
  """
  if key in dict_object.keys():
    return dict_object[key]
  return None

def convert_query_result_to_analytics_model(query_result,student_id,user_id):
  """Convert RowIterator to Analytics Response Model

  Args:
      query_result (RowIterator): _description_
      student_id (str): _description_

  Raises:
      ResourceNotFoundException: _description_

  Returns:
      AnalyticsResponse: return a object of AnalyticsResponse
  """
  course_obj=None
  section_list=[]
  user=None
  flag=True
  for row in query_result:
    flag=False
    row=dict(row)
    if not course_obj or course_obj.course_id!=row[
      "course_id"]:
      if course_obj:
        section_list.append(course_obj)
      else:
        user=AnalyticsUser.parse_obj(row)
        user.user_id=user_id
      course_obj=AnalyticsCourse.parse_obj(row)
    course_work_obj=AnalyticsCourseWork.parse_obj(row)
    if row["submission_id"]:
      submission_obj=AnalyticsSubmission.parse_obj(row)
      course_work_obj.submission=submission_obj
    course_obj.course_work_list.append(course_work_obj)
  if flag:
    raise ResourceNotFoundException(
       f"Analytics Data not found by this {student_id} user")
  if not section_list:
    section_list.append(course_obj)
  return AnalyticsResponse(user=user,section_list=section_list)

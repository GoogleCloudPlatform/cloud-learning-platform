""" Helper Functions"""
import datetime
from fastapi import Depends
from common.utils.auth_service import validate_user_type_and_token, auth_scheme

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


def convert_coursework_to_short_coursework_model(coursework):
  """Convert coursework dict to shortcoursework object
  Args:
      coursework (dict): dict which contains all the coursework details
  Returns:
      dict: dict which contains shortcoursework details
       according to coursework object
  """
  keys = coursework.keys()
  shortCourseWork={}
  shortCourseWork["courseId"] = coursework["courseId"]
  shortCourseWork["courseWorkId"]  = coursework["id"]
  shortCourseWork["title"] = coursework["title"]
  shortCourseWork["state"] = coursework["state"]
  shortCourseWork["creationTime"] = coursework["creationTime"]
  if "materials" in keys:
    shortCourseWork["materials"] = coursework["materials"]
  else:
    shortCourseWork["materials"] = []
  return shortCourseWork


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

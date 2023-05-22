"""User Helper Functions"""
import re
import traceback
from common.models import CourseEnrollmentMapping,CourseTemplateEnrollmentMapping
from common.utils import classroom_crud
from common.utils.errors import (ResourceNotFoundException)
from common.utils.logging_handler import Logger

def course_enrollment_user_model(course_enrollment):
  """Convert Course Enrollment object to Course Enrollment Model"""
  course_enrollment_model = course_enrollment.to_dict()
  course_enrollment_model["course_enrollment_id"] = course_enrollment_model[
      "id"]
  section = course_enrollment_model.pop("section").to_dict()
  course_enrollment_model["section_id"] = section["id"]
  course_enrollment_model["classroom_url"] = section["classroom_url"]
  course_enrollment_model["classroom_id"] = section["classroom_id"]
  course_enrollment_model["cohort_id"] = section["cohort"].to_dict()["id"]
  user = course_enrollment_model.pop("user").to_dict()
  course_enrollment_model["enrollment_status"] = course_enrollment_model.pop(
      "status")
  course_enrollment_model.update(user)
  return course_enrollment_model

def course_template_enrollment_instructional_designer_model(
  course_template_enrollment):
  """Convert Course Template Enrollment to instructional designer Model"""
  course_template_enrollment_model = course_template_enrollment.to_dict()
  course_template_enrollment_model[
    "course_template_enrollment_id"] = course_template_enrollment_model["id"]
  course_template = course_template_enrollment_model.pop(
    "course_template").to_dict()
  course_template_enrollment_model["course_template_id"] = course_template["id"]
  course_template_enrollment_model["classroom_url"] = course_template[
    "classroom_url"]
  course_template_enrollment_model["classroom_id"] = course_template[
    "classroom_id"]
  user = course_template_enrollment_model.pop("user").to_dict()
  course_template_enrollment_model[
    "enrollment_status"] = course_template_enrollment_model.pop("status")
  course_template_enrollment_model.update(user)
  return course_template_enrollment_model

def get_user_id(user, headers):
  regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
  if re.fullmatch(regex, user):
    if classroom_crud.get_user_details_by_email(user_email=user.lower(),
                                                headers=headers)["data"] != []:
      return classroom_crud.get_user_details_by_email(
          user_email=user.lower(), headers=headers)["data"][0]["user_id"]
    else:
      raise ResourceNotFoundException(f"user {user} not found")
  return user


def get_user_email(user, headers):
  regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
  if re.fullmatch(regex, user):
    result = classroom_crud.get_user_details_by_email(user_email=user.lower(),
                                                      headers=headers)["data"]
    if result != []:
      return user.lower(), result[0]["user_id"]
    else:
      raise ResourceNotFoundException(f"user {user} not found")
  return classroom_crud.get_user_details(
      user_id=user, headers=headers)["data"]["email"].lower(), user

def check_user_can_enroll_in_section(email, headers, section):
  """
    Args:
    section :section objects
    email : student email
    headers : Authentication headers
    Returns: boolean value
    True : Student can be enroll

  """
  try:
    student_details = classroom_crud.get_user_details_by_email(
        user_email=email, headers=headers)
  except ResourceNotFoundException as rte:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    Logger.error(rte)
    Logger.info("User is not present in database")
    return True
  # print("Student details____", student_details)
  if student_details["data"] != []:
    user_id = student_details["data"][0]["user_id"]
    result = CourseEnrollmentMapping.check_enrollment_exists_section(
        section_key=section.key, user_id=user_id)
    if result is not None:
      Logger.error(f"User {email} is present in section_id {section.id}")
      return False
  return True

def check_instructional_designer_can_enroll(email, headers, course_template):
  """
    Args:
    course template :course template objects
    email : student email
    headers : Authentication headers
    Returns: boolean value
    True : Student can be enroll

  """
  try:
    user_details = classroom_crud.get_user_details_by_email(
        user_email=email, headers=headers)
  except ResourceNotFoundException as rte:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    Logger.error(rte)
    Logger.info("User is not present in database")
    return True
  if user_details["data"] != []:
    user_id = user_details["data"][0]["user_id"]
    result = CourseTemplateEnrollmentMapping.find_course_enrollment_record(
        course_template_key=course_template.key, user_id=user_id)
    if result is not None:
      Logger.error(f"User {email} is present in"
                   + f" course_template_id {course_template.id}")
      return False
  return True

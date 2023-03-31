"""Student API services"""
import re
import requests
import traceback
from config import USER_MANAGEMENT_BASE_URL
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from common.models import CourseEnrollmentMapping
from common.utils.errors import (ResourceNotFoundException,
UserManagementServiceError)
from common.utils.http_exceptions import (Conflict,InternalServerError)

def get_section_with_minimum_student(sections):
  """Get section with minimum count of students
  Args:
  sections :list of section objects with same cohort
  Returns: sectioons object with minimum count of studnet

  """
  min_sections_count_mapping = None
  min_student = 0
  for i in sections:
    if min_sections_count_mapping is None:
      min_sections_count_mapping = i
      min_student =  i.enrolled_students_count
    else :
      if i.enrolled_students_count < min_student:
        min_student =i.enrolled_students_count
        min_sections_count_mapping = i
  return min_sections_count_mapping

def get_user_id(user,headers):
  regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
  if re.fullmatch(regex, user):
    if classroom_crud.get_user_details_by_email(
        user_email=user.lower(), headers=headers)["data"] != []:
      return classroom_crud.get_user_details_by_email(
          user_email=user.lower(), headers=headers)["data"][0]["user_id"]
    else:
      raise ResourceNotFoundException(f"user {user} not found")
  return user

def get_user_email(user,headers):
  regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
  if re.fullmatch(regex, user):
    result=classroom_crud.get_user_details_by_email(
        user_email=user.lower(), headers=headers)["data"]
    if result != []:
      return user.lower(), result[0]["user_id"]
    else:
      raise ResourceNotFoundException(f"user {user} not found")
  return classroom_crud.get_user_details(
        user_id=user, headers=headers)["data"]["email"].lower(),user

def check_student_can_enroll_in_cohort(email,headers,sections):
  """
    Args:
    sections :list of section objects with from same cohort
    email : student email
    headers : Authentication headers
    Returns: boolean value
    True : Student can be enroll

  """
  try:
    student_details = classroom_crud.get_user_details_by_email(user_email=email,
                                                               headers=headers)
  except ResourceNotFoundException as rte:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    Logger.error(rte)
    Logger.info("Student is not present in database")
    return True
  if student_details["data"] != []:
    user_id = student_details["data"][0]["user_id"]
    for section in sections:
      result = CourseEnrollmentMapping.find_course_enrollment_record(
                            section_key=section.key,
                            user_id=user_id)
      if result is not None:
        Logger.error(f"Student {email} is present in section_id {section.id}")
        return False
  return True

def invite_student(section,student_email,headers):
  """
    Args:
    section :section
    student_email : student email to be invited
    headers : Authentication headers
    Returns: dictionary with course_enrollment_id,user_id,invitation_id,
    cohort_id,section_id,classroom_id,classroom_url

  """
  searched_student = classroom_crud.\
  get_user_details_by_email(user_email=student_email,headers=headers)
  # If the response is success check if student is inactive i.e  raise error
  searched_student = searched_student["data"]
  if searched_student == []:
    Logger.info(f"User {student_email} is not present in database")
    # User does not exist in db call create User API
    body = {
        "first_name":"first_name",
        "last_name": "last_name",
        "email":student_email,
        "user_type": "learner",
        "user_groups": [],
        "status": "active",
        "is_registered": True,
        "failed_login_attempts_count": 0,
        "access_api_docs": False,
        "gaia_id":"",
        "photo_url":""
      }
    create_user_response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
    json=body,headers=headers)
    if create_user_response.status_code !=200:
      raise UserManagementServiceError(
        f"Create User API Error {create_user_response.status_code}")
    user_id = create_user_response.json()["data"]["user_id"]
  else:
    if searched_student[0]["status"] =="inactive":
      raise InternalServerError("Student inactive in \
          database. Please update\
          the student status")
    else:
      user_id = searched_student[0]["user_id"]
      check_already_invited = CourseEnrollmentMapping.\
      find_course_enrollment_record(
              section_key=section.key,user_id=user_id)
      if check_already_invited:
        Logger.error(
          f"Student {student_email} is invide or enrolled in this section")
        raise Conflict(
          f"Student {student_email} is invide or enrolled in this section")
  invitation = classroom_crud.invite_user(course_id=section.classroom_id,
                                        email=student_email,
                                        role="STUDENT")
  Logger.info(f"User with Email {student_email} present with user_id {user_id}")
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.section = section
  course_enrollment_mapping.user = user_id
  course_enrollment_mapping.status = "invited"
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.invitation_id = invitation["id"]
  course_enrollment_id = course_enrollment_mapping.save().id
  return {"invitation_id": invitation["id"],
                  "course_enrollment_id":course_enrollment_id,
                  "user_id":user_id,
                  "section_id":section.id,
                  "cohort_id":section.cohort.key,
            "classroom_id":section.classroom_id,
            "classroom_url":section.classroom_url}

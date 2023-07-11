"""Student API services"""
import requests
import traceback
from config import USER_MANAGEMENT_BASE_URL
from services.section_service import insert_section_enrollment_to_bq
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from common.models import CourseEnrollmentMapping, User
from common.utils.errors import (ResourceNotFoundException,
                                 UserManagementServiceError)
from common.utils.http_exceptions import (Conflict, InternalServerError)


def get_section_with_minimum_student(sections):
  """Get section with minimum count of students
  Args:
  sections :list of section objects with same cohort
  Returns: sections object with minimum count of studnet
  returns none if max student count is reached in all sections
  """
  min_sections_count_mapping = None
  min_student = 0
  for section in sections:
    if min_sections_count_mapping is None:
      if section.enrolled_students_count < section.max_students and\
          section.status =="ACTIVE" and section.enrollment_status=="OPEN":
        min_sections_count_mapping = section
        min_student = section.enrolled_students_count
    else:
      
      if section.enrolled_students_count < min_student and\
        section.enrolled_students_count < section.max_students and\
        section.status =="ACTIVE" and section.enrollment_status=="OPEN":
        min_student = section.enrolled_students_count
        min_sections_count_mapping = section
  return min_sections_count_mapping


def check_student_can_enroll_in_cohort(email, headers, sections):
  """
    Args:
    sections :list of section objects with from same cohort
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
    Logger.info("Student is not present in database")
    return True
  if student_details["data"] != []:
    user_id = student_details["data"][0]["user_id"]
    for section in sections:
      result = CourseEnrollmentMapping.check_enrollment_exists_section(
          section_key=section.key, user_id=user_id)
      if result is not None:
        Logger.error(f"Student {email} is present in section_id {section.id}\
                     enrollment_id {result.id}")
        return False
  return True



def invite_student(section, student_email, headers):
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
        "first_name": "first_name",
        "last_name": "last_name",
        "email": student_email,
        "user_type": "learner",
        "user_groups": [],
        "status": "active",
        "is_registered": True,
        "failed_login_attempts_count": 0,
        "access_api_docs": False,
        "gaia_id": "",
        "photo_url": ""
    }
    create_user_response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
                                         json=body,
                                         headers=headers)
    if create_user_response.status_code != 200:
      raise UserManagementServiceError(
          f"Create User API Error {create_user_response.status_code}")
    user_id = create_user_response.json()["data"]["user_id"]
  else:
    if searched_student[0]["status"] == "inactive":
      raise InternalServerError("Student inactive in \
          database. Please update\
          the student status")
    else:
      user_id = searched_student[0]["user_id"]
      check_already_invited = CourseEnrollmentMapping.\
        check_enrollment_exists_section(
              section_key=section.key,user_id=user_id)
      if check_already_invited:
        Logger.error(
            f"User {student_email} is already invited or "
            + f"enrolled in this section as {check_already_invited.role}")
        raise Conflict(
            f"User {student_email} is invited or enrolled "
            + f"in this section as {check_already_invited.role}")
  invitation = classroom_crud.invite_user(course_id=section.classroom_id,
                                          email=student_email,
                                          role="STUDENT")
  Logger.info(
      f"User with Email {student_email} present with user_id {user_id}")
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.section = section
  course_enrollment_mapping.user = User.find_by_user_id(user_id)
  course_enrollment_mapping.status = "invited"
  course_enrollment_mapping.role = "learner"
  course_enrollment_mapping.invitation_id = invitation["id"]
  course_enrollment_id = course_enrollment_mapping.save().id
  insert_section_enrollment_to_bq(course_enrollment_mapping,section)
  return {
      "invitation_id": invitation["id"],
      "course_enrollment_id": course_enrollment_id,
      "user_id": user_id,
      "section_id": section.id,
      "cohort_id": section.cohort.key,
      "classroom_id": section.classroom_id,
      "classroom_url": section.classroom_url
  }

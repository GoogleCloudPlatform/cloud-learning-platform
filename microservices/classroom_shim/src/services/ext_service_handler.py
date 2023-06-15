from utils.request_handler import get_method
from common.utils.logging_handler import Logger
# pylint: disable=line-too-long, broad-exception-raised


def get_instructional_designers(context_id):
  """Get list of Instructional Designers for a course template"""
  get_ids_url = f"http://lms/lms/api/v1/course_templates/{context_id}/instructional_designers"
  get_ids_res = get_method(url=get_ids_url, use_bot_account=True)

  if get_ids_res.status_code == 200:
    return get_ids_res.json().get("data")
  else:
    Logger.error(
        f"Error 1130 response: Internal error from LMS get IDs API with \
            Status code: {get_ids_res.status_code}; Response: {get_ids_res.text}"
    )
    raise Exception("Request failed with error code 1130")


def get_teachers(context_id):
  """Get list of teachers for a section"""
  get_teachers_members_url = f"http://lms/lms/api/v1/sections/{context_id}/teachers"

  teachers_res = get_method(url=get_teachers_members_url, use_bot_account=True)

  if teachers_res.status_code == 200:
    return teachers_res.json().get("data")
  else:
    Logger.error(
        f"Error 1140 response: Internal error from LMS get students API with \
            Status code: {teachers_res.status_code}; Response: {teachers_res.text}"
    )
    raise Exception("Request failed with error code 1140")


def get_students(context_id):
  """Get list of students for a section"""
  get_student_members_url = f"http://lms/lms/api/v1/sections/{context_id}/students"

  student_res = get_method(url=get_student_members_url, use_bot_account=True)

  if student_res.status_code == 200:
    return student_res.json().get("data")
  else:
    Logger.error(
        f"Error 1150 response: Internal error from LMS get students API \
          Status code: {student_res.status_code}; Response: {student_res.text}")
    raise Exception("Request failed with error code 1150")


def get_course_template_details(context_id):
  """Get details of a course template"""
  get_template_url = f"http://lms/lms/api/v1/course_templates/{context_id}"
  template_res = get_method(url=get_template_url, use_bot_account=True)

  if template_res.status_code == 200:
    context_data = template_res.json()
    context_data["context_type"] = "course_template"
    return context_data
  else:
    Logger.error(
        f"Error 1110: Internal error from LMS course template API with \
          Status code: {template_res.status_code}; Response: {template_res.text}"
    )
    raise Exception("Request failed with error code 1110")


def get_section_details(context_id):
  """Get details of a section"""
  get_section_url = f"http://lms/lms/api/v1/sections/{context_id}"
  section_res = get_method(url=get_section_url, use_bot_account=True)

  if section_res.status_code == 200:
    context_data = section_res.json()
    context_data["description"] = context_data["section"]
    context_data["context_type"] = "section"
    return context_data
  elif section_res.status_code == 404:
    return None
  else:
    Logger.error(f"Error 1120:  Internal error from LMS section API with \
            Status code: {section_res.status_code}; Response: {section_res.text}"
                )
    raise Exception("Request failed with error code 1120")

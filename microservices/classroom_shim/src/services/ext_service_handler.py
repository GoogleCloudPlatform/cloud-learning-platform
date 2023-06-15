from utils.request_handler import get_method, post_method
from common.utils.logging_handler import Logger
# pylint: disable=line-too-long, broad-exception-raised

LMS_BASE_URL = "http://lms/lms/api/v1"
LTI_BASE_URL = "http://lti/lti/api/v1"


def get_course_template_details(context_id):
  """Get details of a course template"""
  get_template_url = f"{LMS_BASE_URL}/course_templates/{context_id}"
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
  get_section_url = f"{LMS_BASE_URL}/sections/{context_id}"
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


def get_instructional_designers(context_id):
  """Get list of Instructional Designers for a course template"""
  get_ids_url = f"{LMS_BASE_URL}/course_templates/{context_id}/instructional_designers"
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
  get_teachers_url = f"{LMS_BASE_URL}/sections/{context_id}/teachers"

  teachers_res = get_method(url=get_teachers_url, use_bot_account=True)

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
  get_students_url = f"{LMS_BASE_URL}/sections/{context_id}/students"

  student_res = get_method(url=get_students_url, use_bot_account=True)

  if student_res.status_code == 200:
    return student_res.json().get("data")
  else:
    Logger.error(
        f"Error 1150 response: Internal error from LMS get students API \
          Status code: {student_res.status_code}; Response: {student_res.text}")
    raise Exception("Request failed with error code 1150")


def get_content_item(content_item_id):
  """Get list of students for a section"""
  get_content_item_url = f"{LTI_BASE_URL}/content-item/{content_item_id}"

  content_item_res = get_method(url=get_content_item_url, use_bot_account=True)

  if content_item_res.status_code == 200:
    return content_item_res.json().get("data")
  else:
    Logger.error(
        f"Error 1300 response: Internal error from LTI get content item API \
          Status code: {content_item_res.status_code}; Response: {content_item_res.text}"
    )
    raise Exception(f"Request failed with code 1300 and the status code is \
            {content_item_res.status_code} with error: {content_item_res.text}")


def copy_content_item(content_item_data):
  """Get list of students for a section"""
  copy_content_item_url = f"{LTI_BASE_URL}/content-item"

  copy_api_res = post_method(
      url=copy_content_item_url,
      request_body=content_item_data,
      use_bot_account=True)

  if copy_api_res.status_code == 200:
    return copy_api_res.json().get("data")
  else:
    Logger.error(
        f"Error 1310 response: Internal error from LTI copy content item API \
          Status code: {copy_api_res.status_code}; Response: {copy_api_res.text}")
    raise Exception(f"Request failed with code 1310 and the status code is \
            {copy_api_res.status_code} and error: {copy_api_res.text}")

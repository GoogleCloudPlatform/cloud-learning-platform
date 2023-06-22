"""External Services Handler"""
from utils.request_handler import get_method, post_method
from common.utils.logging_handler import Logger
# pylint: disable=line-too-long, broad-exception-raised

LMS_BASE_URL = "http://lms/lms/api/v1"
LTI_BASE_URL = "http://lti/lti/api/v1"
USER_MANAGEMENT_BASE_URL = "http://user-management/user-management/api/v1"


def get_user_details(user_email):
  """Get the details of the user"""
  get_user_data_url = f"{USER_MANAGEMENT_BASE_URL}/user/search/email"
  params = {"email": user_email}
  user_data_res = get_method(
      url=get_user_data_url, query_params=params, use_bot_account=True)

  if user_data_res.status_code == 200:
    return user_data_res.json()
  if user_data_res.status_code == 404:
    return None
  else:
    Logger.error(f"Error 1002 response: Internal error from User management \
                 search user API, Status code: {user_data_res.status_code} \
                Response: {user_data_res.text}")
    raise Exception(
        "Request Denied with code 1002, Please contact administrator")


def get_student_details(context_id, user_email):
  """Get the details of the student for a given context"""
  get_student_details_url = f"{LMS_BASE_URL}/v1/sections/{context_id}/students/{user_email}"
  student_details_res = get_method(
      url=get_student_details_url, use_bot_account=True)

  if student_details_res.status_code == 200:
    return student_details_res.json().get("data")
  elif student_details_res.status_code == 404:
    return None
  else:
    Logger.error(
        f"Error 1004 response: Internal error from LMS get students API \
          Status code: {student_details_res.status_code}; Response: {student_details_res.text}"
    )
    raise Exception(
        "Request failed with code 1004, Please contact administrator")


def get_teacher_details(context_id, user_email):
  """Get the details of the teacher for a given context"""
  get_teacher_details_url = f"{LMS_BASE_URL}/sections/{context_id}/teachers/{user_email}"
  teacher_details_res = get_method(
      url=get_teacher_details_url, use_bot_account=True)

  if teacher_details_res.status_code == 200:
    return teacher_details_res.json().get("data")
  elif teacher_details_res.status_code == 404:
    return None
  else:
    Logger.error(
        f"Error 1006 response: Internal error from LMS get teacher details API with \
            Status code: {teacher_details_res.status_code}; Response: {teacher_details_res.text}"
    )
    raise Exception(
        "Request failed with code 1006, Please contact administrator")


def get_instruction_designer_details(context_id, user_email):
  """Get the details of the Instructional designer for a given context"""
  course_template_url = f"{LMS_BASE_URL}/course_templates/{context_id}/instructional_designers/{user_email}"
  course_template_resp = get_method(course_template_url, use_bot_account=True)

  if course_template_resp.status_code == 200:
    return course_template_resp.json()
  else:
    Logger.error(
        f"Error 1013 response: Internal error from LMS get ID details API with \
            Status code: {course_template_resp.status_code}; Response: {course_template_resp.text}"
    )
    raise Exception(
        "Request failed with code 1013, Please contact administrator")


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
    context_data = section_res.json().get("data")
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
  """Get details of a content item"""
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


def list_content_items(context_id=None, tool_id=None):
  """Get the list of content items for a given context and tool"""
  params = {}

  if context_id:
    params["context_id"] = context_id

  if tool_id:
    params["tool_id"] = tool_id

  list_content_items_url = f"{LTI_BASE_URL}/content-items"
  content_item_list_res = get_method(
      url=list_content_items_url, query_params=params, use_bot_account=True)

  if content_item_list_res.status_code == 200:
    return content_item_list_res.json().get("data")
  else:
    Logger.error(
        f"Error 1300 response: Internal error from LTI get content item API \
          Status code: {content_item_list_res.status_code}; Response: {content_item_list_res.text}"
    )
    raise Exception(f"Request failed with code 1300 and the status code is \
            {content_item_list_res.status_code} with error: {content_item_list_res.text}"
                   )


def create_content_item(content_item_data):
  """Create content item with the given data"""
  create_content_item_url = f"{LTI_BASE_URL}/content-item"
  create_api_res = post_method(
      url=create_content_item_url,
      request_body=content_item_data,
      use_bot_account=True)

  if create_api_res.status_code == 200:
    return create_api_res.json().get("data")
  else:
    Logger.error(
        f"Error 1310 response: Internal error from LTI create content item API \
          Status code: {create_api_res.status_code}; Response: {create_api_res.text}"
    )
    raise Exception(f"Request failed with code 1310 and the status code is \
            {create_api_res.status_code} and error: {create_api_res.text}")


def get_lti_tool(tool_id):
  """Get the details of the LTI tool"""
  get_tool_url = f"{LTI_BASE_URL}/tool/{tool_id}"
  tool_res = get_method(url=get_tool_url, use_bot_account=True)

  if tool_res.status_code == 200:
    return tool_res.json().get("data")
  else:
    Logger.error(f"Error 1320 response: Internal error from LTI get tool API \
          Status code: {tool_res.status_code}; Response: {tool_res.text}")
    raise Exception(f"Request failed with code 1320 and the status code is \
            {tool_res.status_code} with error: {tool_res.text}")

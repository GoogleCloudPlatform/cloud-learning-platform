"""Tool Registration Endpoints"""
import requests
from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from config import ERROR_RESPONSES, API_DOMAIN, FIREBASE_API_KEY, FIREBASE_AUTH_DOMAIN, PROJECT_ID
from common.models import LTIAssignment
from common.utils.auth_service import validate_token
from common.utils.secrets import get_backend_robot_id_token
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 UnauthorizedUserError)
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest, Unauthenticated)
from common.utils.logging_handler import Logger
# pylint: disable=line-too-long

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Login Template"], responses=ERROR_RESPONSES)


@router.get("/launch")
def login(request: Request, lti_assignment_id: str):
  """This login endpoint will return the user to firebase login page
  Args:
      lti_assignment_id (str): unique id of the LTI Assignment
  Returns:
      Template response with the login page of the user
  """
  try:
    url = f"{API_DOMAIN}/classroom-shim/api/v1/launch-assignment?lti_assignment_id={lti_assignment_id}"

    lti_assignment = LTIAssignment.find_by_id(lti_assignment_id)
    content_item_url = f"http://lti/lti/api/v1/content-item/{lti_assignment.lti_content_item_id}"
    res = requests.get(
        url=content_item_url,
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)
    data = res.json()
    lti_content_item = data.get("data")

    content_item_info = lti_content_item.get("content_item_info")
    title = content_item_info.get("title")
    if title is None:
      tool_url = f"http://lti/lti/api/v1/tool/{lti_assignment.tool_id}"
      res = requests.get(
          url=tool_url,
          headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
          timeout=60)
      lti_tool = res.json().get("data")
      title = lti_tool.get("name", "")
    return templates.TemplateResponse(
        "login.html", {
            "request": request,
            "redirect_url": url,
            "title": title,
            "firebase_api_key": FIREBASE_API_KEY,
            "project_id": PROJECT_ID,
            "firebase_auth_domain": FIREBASE_AUTH_DOMAIN
        })

  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/launch-assignment")
def launch_assignment(request: Request,
                      lti_assignment_id: Optional[str] = "",
                      user_details: dict = Depends(validate_token)):
  """This launch assignment will take the input assignment id and
  redirect the user to the appropriate LTI tool content item
  Args:
      lti_assignment_id (str): unique id of the LTI Assignment
  Returns:
      Redirects to the LTI tool launch url
  """
  try:
    # verify user if it exists
    user_email = user_details.get("email")
    headers = {"Authorization": request.headers.get("Authorization")}
    fetch_user_request = requests.get(
        "http://user-management/user-management/api/v1/user/search/email",
        params={"email": user_email},
        headers=headers,
        timeout=60)

    if fetch_user_request.status_code == 200:
      faculty_ser_data = fetch_user_request.json().get("data")[0]
    elif fetch_user_request.status_code == 404:
      raise UnauthorizedUserError("Unauthorized")
    else:
      raise Exception("Internal server error from user API")

    user_id = user_data.get("user_id")
    lti_assignment = LTIAssignment.find_by_id(lti_assignment_id)
    lti_content_item_id = lti_assignment.lti_content_item_id

    custom_params = {
        "$ResourceLink.available.startDateTime":
            lti_assignment.start_date.isoformat(),
        "$ResourceLink.submission.endDateTime":
            (lti_assignment.end_date).isoformat(),
        "$ResourceLink.available.endDateTime":
            (lti_assignment.due_date).isoformat()
    }
    # TODO: implementation of "$Context.id.history" as a custom parameter
    # TODO: implementation of "$Person.address.timezone" as a custom parameter
    # TODO: send the user details like profile photo inside final_lti_message_hint_dict and use it in lti service to send as token claims
    final_lti_message_hint_dict = {
        "custom_params_for_substitution": custom_params,
        "user_details": {
            "picture":
                "https://lh3.googleusercontent.com/a/AEdFTp4wIxRnw50hW7_bjiqYOMgdhpt0Gz9dw1D6LpOA=s96-c"
        }
    }

    url = f"{API_DOMAIN}/lti/api/v1/resource-launch-init?lti_content_item_id={lti_content_item_id}&user_id={user_id}"
    # TODO: verify assignment and user relationship
    user_type = user_details.get("user_type")

    if user_type == "learner":
      pass
    elif user_type == "faculty":
      api_url = f"http://lms/lms/api/v1//sections/{lti_assignment.get('section_id')}/teachers/{user_email}"
      fetch_user_mapping = requests.get(api_url, headers=headers, timeout=60)

      if fetch_user_mapping.status_code == 200:
        faculty_data = fetch_user_mapping.json().get("data")
      elif fetch_user_mapping.status_code == 404:
        raise UnauthorizedUserError("Unauthorized")
      else:
        raise Exception(
            "Internal server error from user mapping validation API")

    elif user_type == "admin":
      pass
    return {"url": url, "message_hint": final_lti_message_hint_dict}

  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except UnauthorizedUserError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

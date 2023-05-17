"""Tool Registration Endpoints"""
import traceback
import requests
from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from config import ERROR_RESPONSES, API_DOMAIN, FIREBASE_API_KEY, FIREBASE_AUTH_DOMAIN, PROJECT_ID, auth_client
from common.models import LTIAssignment
from common.utils.auth_service import validate_token
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 UnauthorizedUserError)
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest, Unauthenticated)
from common.utils.logging_handler import Logger
# pylint: disable=line-too-long, unused-variable, broad-exception-raised

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=["Assignment Launch Endpoints"], responses=ERROR_RESPONSES)


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
        headers={"Authorization": f"Bearer {auth_client.get_id_token()}"},
        timeout=60)
    data = res.json()
    lti_content_item = data.get("data")

    content_item_info = lti_content_item.get("content_item_info")
    title = content_item_info.get("title")
    if title is None:
      tool_url = f"http://lti/lti/api/v1/tool/{lti_assignment.tool_id}"
      res = requests.get(
          url=tool_url,
          headers={"Authorization": f"Bearer {auth_client.get_id_token()}"},
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
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get("/launch-assignment")
def launch_assignment(lti_assignment_id: Optional[str] = "",
                      timezone: Optional[str] = "",
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
    headers = {"Authorization": f"Bearer {auth_client.get_id_token()}"}
    fetch_user_request = requests.get(
        "http://user-management/user-management/api/v1/user/search/email",
        params={"email": user_email},
        headers=headers,
        timeout=60)

    if fetch_user_request.status_code == 200:
      user_data = fetch_user_request.json().get("data")[0]
    elif fetch_user_request.status_code == 404:
      raise UnauthorizedUserError(
          "Access Denied with code 1001, Please contact administrator")
    else:
      raise Exception(
          "Request Denied with code 1002, Please contact administrator")

    user_id = user_data.get("user_id")
    lti_assignment = LTIAssignment.find_by_id(lti_assignment_id)
    lti_content_item_id = lti_assignment.lti_content_item_id
    context_id = lti_assignment.context_id

    custom_params = {}
    if lti_assignment.start_date:
      custom_params["$ResourceLink.available.startDateTime"] = (
          lti_assignment.start_date).isoformat()

    if lti_assignment.end_date:
      custom_params["$ResourceLink.available.endDateTime"] = (
          lti_assignment.end_date).isoformat()

    if lti_assignment.due_date:
      custom_params["$ResourceLink.submission.endDateTime"] = (
          lti_assignment.due_date).isoformat()

    if lti_assignment.max_points:
      custom_params["$LineItem.resultValue.max"] = lti_assignment.max_points

    if timezone:
      custom_params["$Person.address.timezone"] = timezone

    if lti_assignment.prev_context_ids:
      context_id_history = ",".join(lti_assignment.prev_context_ids)
      custom_params["$Context.id.history"] = context_id_history

    if lti_assignment.prev_content_item_ids:
      resource_link_id_history = ",".join(lti_assignment.prev_content_item_ids)
      custom_params["$ResourceLink.id.history"] = resource_link_id_history

    url = f"{API_DOMAIN}/classroom-shim/api/v1/launch-assignment?lti_assignment_id={lti_assignment_id}"
    custom_params["$ResourceLink.RelaunchURL"] = url

    if lti_assignment.context_type is None:
      Logger.info(
          f"Request had been failed as the context type is null for {lti_assignment.id}"
      )
      raise Exception(
          "Request failed with code 1010, Please contact administrator")

    final_lti_message_hint_dict = {
        "custom_params_for_substitution": custom_params,
        "context_type": lti_assignment.context_type
    }

    url = f"{API_DOMAIN}/lti/api/v1/resource-launch-init?lti_content_item_id={lti_content_item_id}&user_id={user_id}&context_id={context_id}"
    user_type = user_details.get("user_type")

    if lti_assignment.context_type == "course_template":

      if user_type == "learner":
        raise UnauthorizedUserError(
            "Access Denied with code 1011, Please contact administrator")

      elif user_type in ("faculty", "admin"):
        course_template_url = f"http://lms/lms/api/v1/course_templates/{context_id}"

        course_template_resp = requests.get(
            course_template_url, headers=headers, timeout=60)

        if course_template_resp.status_code == 200:
          course_template_resp_data = course_template_resp.json()
          faculty_list = []
          faculty_list.append(
              course_template_resp_data.get("instructional_designer"))
          faculty_list.append(course_template_resp_data.get("admin"))

          if user_email not in faculty_list:
            raise UnauthorizedUserError(
                "Access Denied with code 1012, Please contact administrator")
        else:
          raise Exception(
              "Request failed with code 1013, Please contact administrator")
      else:
        raise UnauthorizedUserError(
            "Access Denied with code 1014, Please contact administrator")

    else:
      if user_type == "learner":
        api_url = f"http://lms/lms/api/v1/sections/{context_id}/students/{user_email}"
        fetch_user_mapping = requests.get(api_url, headers=headers, timeout=60)

        if fetch_user_mapping.status_code == 200:
          learner_data = fetch_user_mapping.json().get("data")

          if learner_data.get("enrollment_status") == "invited":
            raise UnauthorizedUserError(
                "Enrollment in progress, please retry again after 20 minutes")

        elif fetch_user_mapping.status_code == 404:
          raise UnauthorizedUserError(
              "Access Denied with code 1003, Please contact administrator")
        else:
          raise Exception(
              "Request failed with code 1004, Please contact administrator")

      elif user_type in ("faculty", "admin"):
        api_url = f"http://lms/lms/api/v1/sections/{context_id}/teachers/{user_email}"
        fetch_user_mapping = requests.get(api_url, headers=headers, timeout=60)

        print("fetch_user_mapping.status_code", fetch_user_mapping.status_code)

        if fetch_user_mapping.status_code == 200:
          faculty_data = fetch_user_mapping.json().get("data")
        elif fetch_user_mapping.status_code == 404:
          raise UnauthorizedUserError(
              "Access Denied with code 1005, Please contact administrator")
        else:
          raise Exception(
              "Request failed with code 1006, Please contact administrator")

      else:
        raise UnauthorizedUserError(
            "Access Denied with code 1007, Please contact administrator")

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
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

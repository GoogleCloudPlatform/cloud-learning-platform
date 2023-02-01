"""Tool Registration Endpoints"""
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from config import ERROR_RESPONSES
from common.utils.auth_service import validate_token
from typing import Optional
import requests
# pylint: disable=line-too-long

templates = Jinja2Templates(directory="templates")

router = APIRouter(tags=["Login Template"], responses=ERROR_RESPONSES)


@router.get("/launch")
def login(request: Request, assignment_id: Optional[str] = ""):
  url = "https://core-learning-services-dev.cloudpssolutions.com/classroom-shim/api/v1/launch-assignment"
  if assignment_id is not "":
    url = f"{url}?assignment_id={assignment_id}"
  return templates.TemplateResponse("login.html", {
      "request": request,
      "redirect_url": url
  })


@router.get("/launch-assignment")
def launch_assignment(request: Request,
                      assignment_id: Optional[str] = "",
                      user_details: dict = Depends(validate_token)):
  # verify user if it exists
  user_email = user_details.get("email")
  headers = {"Authorization": request.headers.get("Authorization")}
  fetch_user_request = requests.get(
      "http://user-management/user-management/api/v1/user/search",
      params={"email": user_email},
      headers=headers,
      timeout=60)
  if fetch_user_request.status_code == 200:
    user_data = fetch_user_request.json().get("data")[0]
  elif fetch_user_request.status_code == 404:
    return {"success": False, "message": "User not found"}
  elif fetch_user_request.status_code == 500:
    return {"success": False, "message": "Internal server error"}

  user_id = user_data.get("user_id")
  # TODO: change the content item logic to fetch data from assignments datamodel
  if assignment_id is not "":
    lti_content_item_id = assignment_id
  else:
    lti_content_item_id = "Vwms1o5X2ibH0qdXgnPV"

  clp_domain = "https://core-learning-services-dev.cloudpssolutions.com"
  url = f"{clp_domain}/lti/api/v1/resource-launch-init?lti_content_item_id={lti_content_item_id}&user_id={user_id}"
  # TODO: verify assignment and user relationship
  # TODO: fetch data from request for custom param substitution
  return RedirectResponse(url=url, headers=headers, status_code=302)

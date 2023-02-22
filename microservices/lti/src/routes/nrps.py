"""Line item  Endpoints"""
import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from common.utils.errors import (ResourceNotFoundException, InvalidTokenError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound,
                                          Unauthenticated)
from common.utils.secrets import get_backend_robot_id_token
from schemas.error_schema import NotFoundErrorResponseModel
from services.validate_service import validate_access
# pylint: disable=unused-argument, use-maxsplit-arg, line-too-long

auth_scheme = HTTPBearer(auto_error=False)

router = APIRouter(tags=["NRPS Endpoints"], responses=ERROR_RESPONSES)


@router.get(
    "/{context_id}/memberships",
    name="Get the members of a given context",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(allowed_scopes=[
    "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly"
])
def get_context_members(context_id: str, token: auth_scheme = Depends()):
  """The get context members endpoint will return the list of members data
  with their roles within a given context
  ### Args:
  context_id: `str`
    Unique identifier for context
  ### Raises:
  ResourceNotFoundException:
    If the context does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  LineItem: `LineItemResponseModel`
  """
  try:
    nrps_id = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/memberships"

    get_section_url = f"http://lms/lms/api/v1/sections/{context_id}"

    section_res = requests.get(
        url=get_section_url,
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)

    if section_res.status_code == 200:
      section_data = section_res.json().get("data")
    else:
      raise Exception(
          f"Internal error from LMS get section API with status code - {section_res.status_code}"
      )

    members_list = []
    members_data = []
    get_teachers_members_url = f"http://lms/lms/api/v1/sections/{context_id}/teachers"

    teachers_res = requests.get(
        url=get_teachers_members_url,
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)

    if teachers_res.status_code == 200:
      teachers_data = teachers_res.json().get("data")
    else:
      raise Exception(
          f"Internal error from LMS get teachers API with status code - {teachers_res.status_code}"
      )

    context_details = {
        "id": section_data.get("id"),
        "label": section_data.get("section"),
        "title": section_data.get("description")
    }

    members_data.extend(teachers_data)

    get_student_members_url = f"http://lms/lms/api/v1/sections/{context_id}/students"

    student_res = requests.get(
        url=get_student_members_url,
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)

    if student_res.status_code == 200:
      student_data = student_res.json().get("data")
    else:
      raise Exception(
          f"Internal error from LMS get students API with status code - {student_res.status_code}"
      )

    members_data.extend(student_data)

    for member in members_data:
      members_info = {
          "user_id": member.get("user_id"),
          "status": "Active",
          "given_name": member.get("first_name"),
          "family_name": member.get("last_name"),
          "name": member.get("first_name", "") + member.get("last_name", ""),
          "email": member.get("email"),
          "picture": member.get("photo_url"),
          "lis_person_sourcedid": member.get("user_id")
      }

      if member.get("user_type") == "learner":
        members_info["roles"] = [
            "http://purl.imsglobal.org/vocab/lis/v2/membership#Learner",
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Learner",
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Student"
        ]

      elif member.get("user_type") == "faculty":
        members_info["roles"] = [
            "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor",
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Faculty",
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Instructor"
        ]

      elif member.get("user_type") == "admin":
        members_info["roles"] = [
            "http://purl.imsglobal.org/vocab/lis/v2/membership#Administrator",
            "http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator",
            "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator"
        ]

      members_list.append(members_info)

    output_data = {
        "id": nrps_id,
        "context": context_details,
        "members": members_list
    }

    return output_data

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

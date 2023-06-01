"""NRPS  Endpoints"""
import traceback
import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN, auth_client
from common.utils.errors import (ResourceNotFoundException, InvalidTokenError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound,
                                          Unauthenticated)
from schemas.nrps_schema import GetNRPSModel
from schemas.error_schema import NotFoundErrorResponseModel
from services.validate_service import validate_access
# pylint: disable=unused-argument, use-maxsplit-arg, line-too-long

auth_scheme = HTTPBearer(auto_error=False)

router = APIRouter(tags=["NRPS Endpoints"], responses=ERROR_RESPONSES)


@router.get(
    "/{context_id}/memberships",
    name="Get the members of a given context",
    response_model=GetNRPSModel,
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

    get_context_url = f"http://lms/lms/api/v1/contexts/{context_id}"

    context_res = requests.get(
        url=get_context_url,
        headers={"Authorization": f"Bearer {auth_client.get_id_token()}"},
        timeout=60)

    if context_res.status_code == 200:
      context_data = context_res.json().get("data")
    else:
      Logger.error(
          f"Error 1210: Internal error from Shim service get context API with \
             Status code: {context_res.status_code}; Response: {context_res.text}"
      )
      raise Exception("Request failed with error code 1210")

    context_details = {
        "id": context_data.get("id"),
        "label": context_data.get("description"),
        "title": context_data.get("name")
    }

    context_type = context_data.get("context_type")

    members_list = []
    members_data = []

    get_members_url = f"http://lms/lms/api/v1/contexts/{context_id}/members?context_type={context_type}"
    members_res = requests.get(
        url=get_members_url,
        headers={"Authorization": f"Bearer {auth_client.get_id_token()}"},
        timeout=60)

    if members_res.status_code == 200:
      members_data = members_res.json().get("data")
    else:
      Logger.error(
          f"Error 1220: Internal error from Shim service get members API with \
             Status code: {context_res.status_code}; Response: {context_res.text}"
      )
      raise Exception("Request failed with error code 1220")

    for member in members_data:
      if member.get("user_type") == "learner" and member.get(
          "enrollment_status", "") == "invited":
        pass

      else:
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
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

"""Line item  Endpoints"""
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from config import ERROR_RESPONSES, ISSUER
from common.utils.errors import (ResourceNotFoundException, InvalidTokenError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound,
                                          Unauthenticated)
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
    # TODO: Add API call to check if the context_id exists and get the members
    # data for the given context
    nrps_id = f"{ISSUER}/lti/api/v1/{context_id}/memberships"

    context_details = {
        "id": context_id,
        "label": "Test Course 2",
        "title": "Test title of the course 2",
        "type": ["http://purl.imsglobal.org/vocab/lis/v2/course#CourseOffering"]
    }

    members_list = [{
        "user_id":
            "QXUkLyVRsuJRqFBppUOo",
        "status":
            "Active",
        "given_name":
            "Ross",
        "family_name":
            "Geller",
        "name":
            "Ross Geller",
        "email":
            "ltitesting002@gmail.com",
        "picture":
            "https://lh3.googleusercontent.com/a/AEdFTp5ulzT6ClmwuiTPlpmy6UDm8FrvVoRnWotGi_vn=s100",
        "lis_person_sourcedid":
            "QXUkLyVRsuJRqFBppUOo",
        "roles": ["http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"]
    }, {
        "user_id":
            "MaHmy8jrcpxuF0938EeX",
        "status":
            "Active",
        "given_name":
            "Phoebe",
        "family_name":
            "Buffay",
        "name":
            "Phoebe Buffay",
        "email":
            "ltitesting001@gmail.com",
        "picture":
            "https://lh3.googleusercontent.com/a/AEdFTp4mMFy2EvCqOBrHOXKx_-QlLXq84aoKKo37AsZQ=s100",
        "lis_person_sourcedid":
            "MaHmy8jrcpxuF0938EeX",
        "roles": ["http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"]
    }, {
        "user_id":
            "NSJDWSgXf7nc9H59yWCx",
        "status":
            "Active",
        "given_name":
            "Chandler",
        "family_name":
            "Bing",
        "name":
            "Chandler Bing",
        "email":
            "ltitesting003@gmail.com",
        "picture":
            "https://lh3.googleusercontent.com/a/AEdFTp55udg-hg_3rzF4g7_9frDyWFFA440rs1SAzrPs=s100",
        "lis_person_sourcedid":
            "NSJDWSgXf7nc9H59yWCx",
        "roles": ["http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"]
    }]

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

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
    nrps_id = f"{ISSUER}+/lti/api/v1/{context_id}/memberships"

    context_details = {
        "id": context_id,
        "label": "Test Course",
        "title": "Course1Title",
        "type": [
            "http://purl.imsglobal.org/vocab/lis/v2/course#CourseOffering"
        ]
    }

    members_list = [{
        "name": "Test Learner1",
        "picture": "https://public_image_url1.com",
        "given_name": "Test",
        "family_name": "Learner1",
        "email": "test.learner1@gmail.com",
        "user_id": "qv2py89v21ny8p",
        "lis_person_sourcedid": "qv2py89v21ny8p",
        "roles": ["http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"]
    }, {
        "name":
            "Test Faculty1",
        "picture":
            "https://public_image_url2.com",
        "given_name":
            "Test",
        "family_name":
            "Faculty1",
        "email":
            "test.faculty1@gmail.com",
        "user_id":
            "v23b89ptqvpvqp39y",
        "lis_person_sourcedid":
            "v23b89ptqvpvqp39y",
        "roles": [
            "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor"
        ]
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
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

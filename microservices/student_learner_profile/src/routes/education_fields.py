""" Dropdown endpoints """
import json
from fastapi import APIRouter
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import (InternalServerError,ResourceNotFound)
from schemas.error_schema import NotFoundErrorResponseModel
from schemas.learner_profile_schema import EducationDropdownResponseModel
from config import ERROR_RESPONSES

# pylint: disable = broad-except

router = APIRouter(tags=["Learner Profile"], responses=ERROR_RESPONSES)

@router.get(
    "/learner-profile/education-fields",
    response_model = EducationDropdownResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_education_fields():
  """
  This end point will return the possible options for
  education fields that include education goals, employment status,
   potential career fields

  ### Raises:
  ResourceNotFoundException:
    If the data does not exist
  Exception:
    500 Internal Server Error if something went wrong

  ### Returns:
  dict: Education fields
  """
  try:
    with open("./data/education_fields.json") as json_file:  # pylint: disable=W1514
      education_fields = json.load(json_file)
    return {
  "success": True,
  "message": "Successfully fetched the possible options for"
  " education goals, employment status, potential career fields",
        "data": education_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


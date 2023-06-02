"""Class and methods for fetching inspace token."""
# pylint: disable = broad-exception-raised
import traceback
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
# TODO: Replace TempUser with User once user management is available
from common.models import TempUser
from common.utils.http_exceptions import (InternalServerError,
                              ResourceNotFound, BadRequest)
from common.utils.errors import ResourceNotFoundException, TokenNotFoundError
from common.utils.inspace import (create_inspace_user_helper,
                                  get_inspace_token, get_inspace_user_helper,
                                  is_inspace_enabled)
from common.utils.logging_handler import Logger
from schemas.inpsace_token_schema import InspaceTokenModel
from schemas.error_schema import NotFoundErrorResponseModel
from services.validate_token_service import validate_token
from config import ERROR_RESPONSES

router = APIRouter(tags=["InSpace"],
                   prefix="/inspace",
                   responses=ERROR_RESPONSES)
auth_scheme = HTTPBearer(auto_error=False)


@router.get("/token/{user_id}",
            name="get token",
            response_model=InspaceTokenModel,
            responses={404: {
            "model": NotFoundErrorResponseModel
           }})
def get_token(user_id: str, token: auth_scheme = Depends()):
  """The get users endpoint will return the token for inspace
    ### Args:
       user_id (str): Unique identifier for user

    ### Raises:
      ResourceNotFoundException: If the user does not exist
      Exception: 500 Internal Server Error if something went wrong

    ### Returns:
      InspaceTokenModel: token Object
  """
  try:
    if token:
      token_dict = dict(token)
      id_token = token_dict.get("credentials")
      if id_token:
        validate_token(id_token)
      else:
        raise TokenNotFoundError("Token not found")
    else:
      raise TokenNotFoundError("Token not found")

    if not is_inspace_enabled():
      raise Exception("you don't have permission to access this endpoint")

    user = TempUser.find_by_user_id(user_id)
    if user.inspace_user is None or \
      user.inspace_user["is_inspace_user"] is False:
      raise Exception(f"Inspace user does not exist for user id {user_id}")

    if user.inspace_user["inspace_user_id"] != "":
      token_response = get_inspace_token(user_id)
    else:
      status_code, inspace_user_res = get_inspace_user_helper(user)
      if status_code == 200:
        inspace_user = {
          "is_inspace_user": True,
          "inspace_user_id": inspace_user_res["inspaceUser"]["id"],
        }
        user.inspace_user = inspace_user
        user.update()
        token_response = get_inspace_token(user_id)
      else:
        if create_inspace_user_helper(user):
          token_response = get_inspace_token(user_id)
        else:
          raise Exception(f"Inspace user does not exist for user id {user_id}")

    if token_response.status_code == 200:
      return {
        "success": True,
        "message": "Successfully fetched the inspace token",
        "data": token_response.json()
      }
    else:
      raise Exception(token_response.json()["error"])

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except TokenNotFoundError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

"""Class and methods for handling generate route."""

from services.refresh_token_service import generate_token
from services.firebase_authentication import verify_token
from utils.exception_handler import InvalidRefreshTokenError
from fastapi import APIRouter
from schemas.generate_token_schema import (GenerateTokenResponseModel,
                                           GenerateTokenRequestModel)
from common.utils.http_exceptions import (InvalidToken, InternalServerError)
from common.models import TempUser
from config import ERROR_RESPONSES

# pylint: disable = broad-exception-raised
router = APIRouter(
    tags=["RefreshToken"],
    responses=ERROR_RESPONSES)


@router.post("/generate", response_model=GenerateTokenResponseModel)
def generate_id_token(input_params: GenerateTokenRequestModel):
  """Generates IdToken from the Refresh token received

  Args:
      refresh_token(str): refresh token
      input_params(dict): GenerateTokenRequestModel

  Returns:
      GenerateTokenResponseModel: Contains access token, idToken and their
      expiry time.

  Parameters
  ----------
  """
  try:
    input_dict = {**input_params.dict()}
    token_resp = generate_token(input_dict)

    decoded_token = verify_token(token_resp["id_token"])
    user = TempUser.find_by_email(decoded_token["email"])
    token_resp["user_id"] = user.user_id
    return {
        "success": True,
        "message": "Token generated successfully",
        "data": token_resp
    }
  except InvalidRefreshTokenError as e:
    raise InvalidToken(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

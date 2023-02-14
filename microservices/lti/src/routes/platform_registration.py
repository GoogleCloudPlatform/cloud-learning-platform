"""Platform Registration endpoints"""
from fastapi import APIRouter
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from common.models import Platform
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict)
from schemas.platform_schema import (PlatformModel, PlatformResponseModel,
                                     UpdatePlatformModel, DeletePlatform,
                                     PlatformSearchResponseModel,
                                     AllPlatformsResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel

router = APIRouter(
    tags=["Platform Registration Endpoints"], responses=ERROR_RESPONSES)


def add_tool_key_set(fields, uuid):
  fields["tool_url"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1"
  fields["tool_login_url"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/oidc-login"
  fields["tool_keyset_url"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/jwks/{uuid}"
  return fields


@router.get("/platform/search", response_model=PlatformSearchResponseModel)
def search_platform(client_id: str):
  """Search for Platform based on the client_id
  ### Args:
  client_id: `str`
    Client ID of the Platform.
  ### Raises:
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  List of Platform: `PlatformSearchResponseModel`
  """
  result = []
  try:
    # fetch platform that matches client_id
    platform = Platform.find_by_client_id(client_id)
    if platform:
      platform_fields = platform.get_fields(reformat_datetime=True)
      platform_fields = add_tool_key_set(platform_fields, platform.id)
      platform_fields["id"] = platform.id
      result = [platform_fields]
    return {
        "success": True,
        "message": "Successfully fetched the platforms",
        "data": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/platforms",
    name="Get all platforms",
    response_model=AllPlatformsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_platforms(skip: int = 0, limit: int = 10):
  """The get platforms endpoint will return an array of platforms from firestore
  ### Args:
  skip: `int`
    Number of platforms to be skipped <br/>
  limit: `int`
    Size of platforms array to be returned <br/>
  ### Raises:
  ValueError:
    Raised when input args are outside range. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Array of Platforms: `AllPlatformsResponseModel`
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    collection_manager = Platform.collection.filter("deleted_at_timestamp",
                                                    "==", None)
    platforms = collection_manager.order("-created_time").offset(skip).fetch(
        limit)

    platforms_list = []
    for platform in platforms:
      platform_fields = platform.get_fields(reformat_datetime=True)
      platform_fields = add_tool_key_set(platform_fields, platform.id)
      platform_fields["id"] = platform.id
      platforms_list.append(platform_fields)
    return {
        "success": True,
        "message": "Platforms has been fetched successfully",
        "data": platforms_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/platform/{platform_id}",
    name="Get a specific platform",
    response_model=PlatformResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_platform(platform_id: str):
  """The get platform endpoint will return the platform
  from firestore of which platform_id is provided
  ### Args:
  platform_id: `str`
    Unique identifier for platform
  ### Raises:
  ResourceNotFoundException:
    If the platform with given platform_id does not exist. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Platform: `PlatformResponseModel`
  """
  try:
    platform = Platform.find_by_id(platform_id)
    platform_fields = platform.get_fields(reformat_datetime=True)
    platform_fields = add_tool_key_set(platform_fields, platform_id)
    platform_fields["id"] = platform.id
    return {
        "success":
            True,
        "message":
            f"Platform with '{platform_id}' has been fetched successfully",
        "data":
            platform_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/platform",
    name="Register a Platform",
    response_model=PlatformResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_platform(input_platform: PlatformModel):
  """The create platform endpoint will add the platform to the firestore if it
  does not exist.If any platform exist with same issuer then it will
  raise ConflictError
  ### Args:
  input_platform: `PlatformModel`
    Input platform to be inserted
  ### Raises:
  ConflictError:
    Raised if any platform with same issuer exist <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Platform Data: `PlatformResponseModel`
  """
  # TODO: Currently the issuer should be unique. But later, the combination of
  # client_id and issuer should be unique
  try:
    input_platform_dict = {**input_platform.dict()}
    issuer = input_platform_dict.get("issuer")
    platform = Platform.find_by_issuer(issuer)

    if platform:
      error_msg = f"Platform with the provided issuer '{issuer}' already exists"
      raise ConflictError(error_msg)

    new_platform = Platform()
    new_platform = new_platform.from_dict(input_platform_dict)
    new_platform.save()
    platform_fields = new_platform.get_fields(reformat_datetime=True)
    platform_fields = add_tool_key_set(platform_fields, new_platform.id)
    platform_fields["id"] = new_platform.id
    return {
        "success": True,
        "message": "Platform has been created successfully",
        "data": {
            **platform_fields
        }
    }
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/platform/{platform_id}",
    response_model=PlatformResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_platform(platform_id: str, input_platform: UpdatePlatformModel):
  """Update a platform
  ### Args:
  platform_id: `str`
    Unique identifier for platform
  input_platform: `UpdatePlatformModel`
    Required body of the platform
  ### Raises:
  ResourceNotFoundException:
    If the platform with given platform_id does not exist <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Updated Platform: `PlatformResponseModel`
  """
  try:
    existing_platform = Platform.find_by_id(platform_id)
    platform_fields = existing_platform.get_fields()

    input_platform_dict = {**input_platform.dict()}

    if not input_platform_dict.get(
        "platform_public_key") and not input_platform_dict.get(
            "platform_keyset_url"):
      return {"success": False, "message": "Public key is missing", "data": []}

    for key, value in input_platform_dict.items():
      platform_fields[key] = value
    for key, value in platform_fields.items():
      setattr(existing_platform, key, value)
    existing_platform.update()
    platform_fields = existing_platform.get_fields(reformat_datetime=True)
    platform_fields = add_tool_key_set(platform_fields, platform_id)
    platform_fields["id"] = existing_platform.id
    return {
        "success": True,
        "message": "Successfully updated the platform",
        "data": platform_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/platform/{platform_id}",
    response_model=DeletePlatform,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_platform(platform_id: str):
  """Delete a platform from firestore
  ### Args:
  platform_id: `str`
    Unique ID of the platform
  ### Raises:
  ResourceNotFoundException:
    If the platform with given platform_id does not exist. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    Platform.find_by_id(platform_id)
    Platform.delete_by_id(platform_id)
    return {}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

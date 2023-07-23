"""
  Badge endpoints
"""
from fastapi import APIRouter, UploadFile, File
from schemas.badge_schema import (BadgeModel, BadgeResponseModel,
                                  AllBadgeResponseModel, DeleteBadge,
                                  BadgeImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from common.models.credential_pathway_model import BadgeClass
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError, PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict,
                                          PayloadTooLarge)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

# pylint: disable = broad-except

router = APIRouter(
    tags=["Badge"],
    responses=ERROR_RESPONSES)


@router.get(
    "/badge", response_model=AllBadgeResponseModel, name="Get all Badges")
def get_all_badges(skip: int = 0, limit: int = 10):
  """The get Badges endpoint will return an array of Badge from firestore

    Args:
        skip (int): Number of objects to be skipped
        limit (int): Size of badge array to be returned

    Raises:
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        AllBadgeResponseModel: Array of badge Object
    """
  try:

    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    badges = BadgeClass.collection.order("-created_time").offset(skip).fetch(
        limit)
    badges = [i.get_fields(reformat_datetime=True) for i in badges]

    return {
        "success": True,
        "message": "Successfully fetched the badges",
        "data": badges
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/badge/{uuid}",
    response_model=BadgeResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_badge(uuid: str):
  """The get badge endpoint will return the badge from
    firestore of which uuid is provided

    Args:
        uuid (str): Unique identifier for badge

    Raises:
        ResourceNotFoundException: If the badge does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        BadgeResponseModel: Badge Object
    """
  try:

    badge = BadgeClass.find_by_uuid(uuid)
    badge_fields = badge.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the badge",
        "data": badge_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/badge",
    response_model=BadgeResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_badge(input_badge: BadgeModel):
  """The create Badge endpoint will add the given Badge in request body to
    the firestore

    Args:
        input_badge (Badge): input Badge to be inserted

    Raises:
        ResourceNotFoundException: If the Badge does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        BadgeResponseModel: Badge Object
    """
  try:
    new_badge = BadgeClass()
    input_badge_dict = {**input_badge.dict()}
    badge = BadgeClass.collection.filter("entity_id", "==",
                                         input_badge_dict["entity_id"]).get()

    # Checking if a badge document already exists with the same entity id

    if badge is not None:
      raise ConflictError(f"Learner with the given badge id"
                          f":{input_badge_dict['entityId']} already exists")

    new_badge = new_badge.from_dict(input_badge_dict)
    new_badge.uuid = ""
    new_badge.save()
    new_badge.uuid = new_badge.id
    new_badge.update()
    badge_fields = new_badge.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully create the Badges",
        "data": badge_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except ConflictError as e:
    raise Conflict(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/badge/{uuid}",
    response_model=BadgeResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_badge(uuid: str, input_badge: BadgeModel):
  """Update a badge with the uuid passed in the request body

    Args:
        uuid (str): Unique identifier for badge
        request (Badge): Required body of the
        badge

    Raises:
        ResourceNotFoundException: If the badge does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        BadgeResponseModel: Badge Object
    """
  try:
    existing_badge = BadgeClass.find_by_uuid(uuid)

    input_badge_dict = {**input_badge.dict()}
    badge_fields = existing_badge.get_fields()
    for key, value in input_badge_dict.items():
      if value is not None:
        badge_fields[key] = value
    for key, value in badge_fields.items():
      setattr(existing_badge, key, value)
    existing_badge.update()
    badge_fields = existing_badge.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully update the badge",
        "data": badge_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/badge/{uuid}",
    response_model=DeleteBadge,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_badge(uuid: str):
  """Delete a badge with the given uuid from firestore

    Args:
        uuid (str): Unique id of the badge

    Raises:
        ResourceNotFoundException: If the badge does not exist
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        DeleteBadge: Response Message
    """
  try:
    badge = BadgeClass.find_by_uuid(uuid)
    BadgeClass.collection.delete(badge.key)
    return {"success": True, "message": "Successfully deleted the badge"}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/badge/import/json",
    response_model=BadgeImportJsonResponse,
    name="Import Badge from JSON file",
    responses={413: {
      "model": PayloadTooLargeResponseModel
    }})
async def import_badge(json_file: UploadFile = File(...)):
  """Create badge from json file

    Args:
      json_file (UploadFile): Upload json file consisting of badge.
      json_schema should match Badge

    Raises:
      Exception: 500 Internal Server Error if something fails

    Returns:
        BadgeImportJsonResponse: Array of uuid's
    """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BadgeModel,
        model_obj=BadgeClass,
        object_name="badges")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

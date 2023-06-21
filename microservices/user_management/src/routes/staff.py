""" Staff endpoints """

import traceback
import re
import json
from fastapi import APIRouter, UploadFile, File, Query
from common.models import Staff
from common.utils.logging_handler import Logger
from common.utils.errors import (ConflictError, ResourceNotFoundException,
                                ValidationError, PayloadTooLargeError)
from common.utils.http_exceptions import (Conflict, InternalServerError,
                                          BadRequest, ResourceNotFound,
                                          PayloadTooLarge)
from schemas.staff_schema import (StaffSearchResponseModel,
                                  AllStaffResponseModel,
                                  GetStaffResponseModel,
                                  PostStaffResponseModel,
                                  BasicStaffModel, UpdateStaffResponseModel,
                                  UpdateStaffModel, DeleteStaffReponseModel,
                                  StaffImportJsonResponse,
                                  ProfileFieldsResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import_non_user
from services.staff import create_staff, update_staff
from config import ERROR_RESPONSES, PAYLOAD_FILE_SIZE


router = APIRouter(tags=["Staff"], responses=ERROR_RESPONSES)

@router.get("/staff/search", response_model=StaffSearchResponseModel)
def search_staff_by_email(email: str):
  """
  Search for Staff based on the email

  Args:
    email (str): Email id of the Staff.

  Returns:
    StaffSearchResponseModel: List of Staff objects
  """
  try:
    result = []
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

    email_match = re.compile(pattern=pattern)

    if not email_match.fullmatch(email):
      raise ValidationError(f"Invalid staff email ID format: {email}")

    staff = Staff.find_by_email(email)
    if staff:
      result = [staff.get_fields(reformat_datetime=True)]
    return {
        "success": True,
        "message": "Successfully fetched the staff",
        "data": result
    }

  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get("/staffs",
  response_model=AllStaffResponseModel,
  name="Get all Staffs")
def get_staffs(skip: int = Query(0, ge=0, le=2000),
              limit: int = Query(10, ge=1, le=100)):
  """
  This endpoint will return an array of staffs from firestore

  Args:
    skip (int): Number of objects to be skipped
    limit (int): Size of staff array to be returned

  Raises:
    ValidationError: 422 BadRequest if invalid values are given are parameters
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    AllStaffResponseModel: Array of Staff Object
  """
  try:
    collection_manager = Staff.collection.filter("is_deleted", "==", False)

    staffs = collection_manager.order("-created_time").offset(skip).fetch(limit)
    staffs = [i.get_fields(reformat_datetime=True) for i in staffs]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": staffs
    }
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/staff/{uuid}",
    response_model=GetStaffResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_staff(uuid: str):
  """
  This endpoint will return the staff from firestore of which uuid is provided

  Args:
    uuid (str): Unique identifier for staff

  Raises:
    ResourceNotFoundException: If the staff does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    GetStaffResponseModel: staff Object
  """
  try:
    staff = Staff.find_by_uuid(uuid)
    staff_fields = staff.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the staff",
        "data": staff_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/staff", response_model=PostStaffResponseModel)
def create_staff_api(input_staff: BasicStaffModel):
  """
  This endpoint will add the staff in request body to the firestore

  Args:
    input_staff (BasicStaffModel): input staff to be inserted

  Raises:
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    PostStaffResponseModel: Staff Object
  """
  try:
    staff = create_staff(input_staff)
    return {
        "success": True,
        "message": "Successfully created staff",
        "data": staff
    }
  except ConflictError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/staff/{uuid}",
    response_model=UpdateStaffResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_staff_api(uuid: str, input_staff: UpdateStaffModel):
  """
  Update a staff with the uuid passed in the request body

  Args:
    input_staff (UpdateStaffModel): Required body of the staff

  Raises:
    ResourceNotFoundException: If the staff does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    UpdateStaffResponseModel: Staff Object
  """
  try:
    staff_fields = update_staff(uuid, input_staff)

    return {
        "success": True,
        "message": "Successfully updated the staff",
        "data": staff_fields
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/staff/{uuid}",
    response_model=DeleteStaffReponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_staff(uuid: str):
  """
  Delete a staff with the given uuid from firestore

  Args:
    uuid (str): Unique id of the staff

  Raises:
    ResourceNotFoundException: If the staff does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    JSON: Success/Fail Message
  """
  try:
    Staff.delete_by_uuid(uuid)
    return {"success": True, "message": "Successfully deleted the staff"}
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/staff/import/json",
    response_model=StaffImportJsonResponse,
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }},
    name="Import Staffs from JSON file")
async def import_staffs(json_file: UploadFile = File(...)):
  """Create staffs from json file

  Args:
    json_file (UploadFile): Upload json file consisting of staffs.
    json_schema should match BasicStaffModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    StaffImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import_non_user(
        json_file=json_file,
        json_schema=BasicStaffModel,
        model_obj=Staff,
        object_name="staffs")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/staff/profile/fields",
    response_model=ProfileFieldsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }},
    name="Fetch Profile Fields")
def get_profile_fields():
  """Fetch all possible options for following profile fields:
    - pronouns
    - workdays
    - timezones

  Args:
    None

  Raises:
    ResourceNotFoundException: If the data does not exist
    Exception: 500 Internal Server Error if something fails

  Returns:
    dict: Profile fields
  """
  try:
    with open("./data/profile_fields.json", encoding="utf-8") as json_file:
      profile_fields = json.load(json_file)
    return {
  "success": True,
  "message": "Successfully fetched the possible options for"
    " pronouns, workdays, timezones",
        "data": profile_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

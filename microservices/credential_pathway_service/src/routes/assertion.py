"""
  Assertion endpoints
"""
from fastapi import APIRouter, UploadFile, File
from schemas.assertion_schema import (AssertionModel, AssertionResponseModel,
                                      AllAssertionResponseModel,
                                      DeleteAssertion,
                                      AssertionImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from common.models.credential_pathway_model import Assertion
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError, PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict,
                                          PayloadTooLarge)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

# pylint: disable = broad-except
# pylint: disable = line-too-long

router = APIRouter(
    tags=["Assertion"],
    responses=ERROR_RESPONSES)


@router.get(
    "/assertion",
    response_model=AllAssertionResponseModel,
    name="Get all Assertion")
def get_all_assertion(skip: int = 0, limit: int = 10):
  """The get Assertion endpoint will return an array of assertion from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of assertion array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllAssertionResponseModel: Array of assertion Object
  """
  try:

    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    assertion = Assertion.collection.order("-created_time").offset(skip).fetch(
        limit)
    assertion = [i.get_fields(reformat_datetime=True) for i in assertion]

    return {
        "success": True,
        "message": "Successfully fetched the Assertions",
        "data": assertion
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/assertion/{uuid}",
    response_model=AssertionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_assertion(uuid: str):
  """The get assertion endpoint will return the assertion from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for assertion

  Raises:
      ResourceNotFoundException: If the assertion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AssertionResponseModel: Assertion Object
  """
  try:

    assertion = Assertion.find_by_uuid(uuid)
    assertion_fields = assertion.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the assertion",
        "data": assertion_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/assertion",
    response_model=AssertionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_assertion(input_assertion: AssertionModel):
  """The create Assertion endpoint will add the given Assertion in request body to
  the firestore

  Args:
      request (Assertion): input Assertion to be
      inserted

  Raises:
      ResourceNotFoundException: If the Assertion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AssertionResponseModel: Assertion Object
  """
  try:

    new_assertion = Assertion()
    input_assertion_dict = {**input_assertion.dict()}
    assertion = Assertion.collection.filter(
        "entity_id", "==", input_assertion_dict["entity_id"]).get()

    # Checking if a assertion document already exists with the same entity id

    if assertion is not None:
      raise ConflictError(f"Learner with the given assertion id"
                          f":{input_assertion_dict['entity_id']} already "
                          f"exists")

    new_assertion = new_assertion.from_dict(input_assertion_dict)
    new_assertion.uuid = ""
    new_assertion.save()
    new_assertion.uuid = new_assertion.id
    new_assertion.update()
    assertion_fields = new_assertion.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully create the Assertions",
        "data": assertion_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except ConflictError as e:
    raise Conflict(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/assertion/{uuid}",
    response_model=AssertionResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_assertion(uuid: str, input_assertion: AssertionModel):
  """Update a assertion with the uuid passed in the request body

  Args:
      uuid (str): Unique identifier for assertion
      request (Assertion): Required body of the
      assertion

  Raises:
      ResourceNotFoundException: If the assertion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AssertionResponseModel: Assertion Object
  """
  try:

    existing_assertion = Assertion.find_by_uuid(uuid)

    input_assertion_dict = {**input_assertion.dict()}
    assertion_fields = existing_assertion.get_fields()
    for key, value in input_assertion_dict.items():
      if value is not None:
        assertion_fields[key] = value
    for key, value in assertion_fields.items():
      setattr(existing_assertion, key, value)
    existing_assertion.update()
    assertion_fields = existing_assertion.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully update the assertion",
        "data": assertion_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/assertion/{uuid}",
    response_model=DeleteAssertion,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_assertion(uuid: str):
  """Delete a assertion with the given uuid from firestore

  Args:
      uuid (str): Unique id of the assertion

  Raises:
      ResourceNotFoundException: If the assertion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      DeleteAssertion: Response Message
  """
  try:

    assertion = Assertion.find_by_uuid(uuid)
    Assertion.collection.delete(assertion.key)

    return {"success": True, "message": "Successfully deleted the assertion"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/assertion/import/json",
    response_model=AssertionImportJsonResponse,
    name="Import Assertion from JSON file",
    responses={413: {
      "model": PayloadTooLargeResponseModel
    }})
async def import_assertion(json_file: UploadFile = File(...)):
  """Create assertion from json file

  Args:
    json_file (UploadFile): Upload json file consisting of assertion.
    json_schema should match Assertion

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      AssertionImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=AssertionModel,
        model_obj=Assertion,
        object_name="assertions")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

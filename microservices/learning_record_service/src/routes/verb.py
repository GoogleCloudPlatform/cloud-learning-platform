""" Verb endpoints """
from fastapi import APIRouter, UploadFile, File, Query
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                ConflictError, PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict,
                                          PayloadTooLarge)
from common.models import Verb
from services.json_import import json_import
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from schemas.verb_schema import (VerbModel, BasicVerbModel, UpdateVerbModel,
                                 AllVerbsResponseModel, GetVerbResponseModel,
                                 PostVerbResponseModel, UpdateVerbResponseModel,
                                 DeleteVerb, VerbImportJsonResponse)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Verb"],
    responses=ERROR_RESPONSES)


@router.get(
    "/verbs", response_model=AllVerbsResponseModel, name="Get All Verbs")
def get_verbs(skip: int = Query(0, ge=0, le=2000),
              limit: int = Query(10, ge=1, le=100)):
  """The get verbs endpoint will return an array verbs from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of verb array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllVerbsResponseModel: Array of Verb Object
  """
  try:
    collection_manager = Verb.collection

    verbs = collection_manager.order("-created_time").offset(skip).fetch(limit)
    verbs = [i.get_fields(reformat_datetime=True) for i in verbs]
    count = 10000
    response = {"records": verbs, "total_count": count}
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/verb/{uuid}",
    response_model=GetVerbResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_verb(uuid: str):
  """The get verb endpoint will return the verb from firestore of which uuid
  is provided

  Args:
      uuid (str): Unique identifier for verb

  Raises:
      ResourceNotFoundException: If the verb does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetVerbResponseModel: verb Object
  """
  try:
    verb = Verb.find_by_uuid(uuid)
    verb_fields = verb.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the verb",
        "data": verb_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/verb", response_model=PostVerbResponseModel)
def create_verb(input_verb: VerbModel):
  """The post verb endpoint will add the given verb in request body to the
  firestore

  Args:
      input_verb (VerbModel): input verb to be inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostVerbResponseModel: Verb Object
  """
  try:
    input_verb_dict = {**input_verb.dict()}
    verb = Verb.find_by_name(input_verb_dict["name"])
    if verb is None:
      new_verb = Verb()
      new_verb = new_verb.from_dict(input_verb_dict)
      new_verb.uuid = ""
      new_verb.save()
      new_verb.uuid = new_verb.id
      new_verb.update()

      verb_fields = new_verb.get_fields(reformat_datetime=True)

      return {
          "success": True,
          "message": "Successfully created the verb",
          "data": verb_fields
      }
    else:
      raise ConflictError(
        f"Verb with the given name {input_verb_dict['name']} already exists"
        )

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/verb/{uuid}",
    response_model=UpdateVerbResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_verb(uuid: str, input_verb: UpdateVerbModel):
  """Update a verb with the uuid passed in the request body

  Args:
      input_verb (UpdateVerbModel): Required body of the verb

  Raises:
      ResourceNotFoundException: If the verb does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateVerbResponseModel: Verb Object
  """
  try:
    existing_verb = Verb.find_by_uuid(uuid)

    input_verb_dict = {**input_verb.dict(exclude_unset=True)}
    verb_fields = existing_verb.get_fields()

    for key, value in input_verb_dict.items():
      verb_fields[key] = value
    for key, value in verb_fields.items():
      setattr(existing_verb, key, value)

    existing_verb.update()
    verb_fields = existing_verb.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the verb",
        "data": verb_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/verb/{uuid}",
    response_model=DeleteVerb,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_verb(uuid: str):
  """Delete a verb with the given uuid from firestore

  Args:
      uuid (str): Unique id of the verb

  Raises:
      ResourceNotFoundException: If the actvity does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    verb = Verb.find_by_uuid(uuid)

    Verb.collection.delete(verb.key)

    return {"success": True, "message": "Successfully deleted the verb"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/verb/import/json",
    response_model=VerbImportJsonResponse,
    name="Import Verbs from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_verbs(json_file: UploadFile = File(...)):
  """Create verbs from json file

  Args:
    json_file (UploadFile): Upload json file consisting of verbs.
    json_schema should match BasicVerbModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      VerbImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicVerbModel,
        model_obj=Verb,
        object_name="verbs")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

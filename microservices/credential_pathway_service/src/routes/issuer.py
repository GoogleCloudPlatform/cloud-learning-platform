"""
  Issuer endpoints
"""
from fastapi import APIRouter, UploadFile, File
from schemas.issuer_schema import (IssuerModel, IssuerResponseModel,
                                   AllIssuerResponseModel, DeleteIssuer,
                                   IssuerImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from common.models.credential_pathway_model import Issuer
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError, PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict,
                                          PayloadTooLarge)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

# pylint: disable = broad-except

router = APIRouter(
    tags=["Issuer"],
    responses=ERROR_RESPONSES)


@router.get(
    "/issuer", response_model=AllIssuerResponseModel, name="Get all Issuer")
def get_all_issuer(skip: int = 0, limit: int = 10):
  """The get Issuer endpoint will return an array of issuer from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of issuer array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllIssuerResponseModel: Array of issuer Object
  """
  try:

    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    issuers = Issuer.collection.order("-created_time").offset(skip).fetch(limit)
    issuers = [i.get_fields(reformat_datetime=True) for i in issuers]
    return {
        "success": True,
        "message": "Successfully fetched the Issuers",
        "data": issuers
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/issuer/{uuid}",
    response_model=IssuerResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_issuer(uuid: str):
  """The get issuer endpoint will return the issuer from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for issuer

  Raises:
      ResourceNotFoundException: If the issuer does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      IssuerResponseModel: Issuer Object
  """
  try:

    issuer = Issuer.find_by_uuid(uuid)
    issuer_fields = issuer.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the issuer",
        "data": issuer_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/issuer",
    response_model=IssuerResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_issuer(input_issuer: IssuerModel):
  """The create Issuer endpoint will add the given Issuer in request body to
  the firestore

  Args:
      request (Issuer): input Issuer to be
      inserted

  Raises:
      ResourceNotFoundException: If the Issuer does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      IssuerResponseModel: Issuer Object
  """
  try:
    new_issuer = Issuer()
    input_issuer_dict = {**input_issuer.dict()}
    issuer = Issuer.collection.filter("entity_id", "==",
                                      input_issuer_dict["entity_id"]).get()

    # Checking if a issuer document already exists with the same entity id

    if issuer is not None:
      raise ConflictError(f"Learner with the given issuer id"
                          f":{input_issuer_dict['entity_id']} already exists")

    new_issuer = new_issuer.from_dict(input_issuer_dict)
    new_issuer.uuid = ""
    new_issuer.save()
    new_issuer.uuid = new_issuer.id
    new_issuer.update()
    issuer_fields = new_issuer.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully create the Issuers",
        "data": issuer_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except ConflictError as e:
    raise Conflict(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/issuer/{uuid}",
    response_model=IssuerResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_issuer(uuid: str, input_issuer: IssuerModel):
  """Update a issuer with the uuid passed in the request body

  Args:
      uuid (str): Unique identifier for issuer
      request (Issuer): Required body of the
      issuer

  Raises:
      ResourceNotFoundException: If the issuer does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      IssuerResponseModel: Issuer Object
  """
  try:
    existing_issuer = Issuer.find_by_uuid(uuid)

    input_issuer_dict = {**input_issuer.dict()}
    issuer_fields = existing_issuer.get_fields()
    for key, value in input_issuer_dict.items():
      if value is not None:
        issuer_fields[key] = value
    for key, value in issuer_fields.items():
      setattr(existing_issuer, key, value)
    existing_issuer.update()
    issuer_fields = existing_issuer.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully update the issuer",
        "data": issuer_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/issuer/{uuid}",
    response_model=DeleteIssuer,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_issuer(uuid: str):
  """Delete a issuer with the given uuid from firestore

  Args:
      uuid (str): Unique id of the issuer

  Raises:
      ResourceNotFoundException: If the issuer does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      DeleteIssuer: Response Message
  """
  try:

    issuer = Issuer.find_by_uuid(uuid)
    Issuer.collection.delete(issuer.key)

    return {"success": True, "message": "Successfully deleted the issuer"}

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/issuer/import/json",
    response_model=IssuerImportJsonResponse,
    name="Import Issuer from JSON file",
    responses={413: {
      "model": PayloadTooLargeResponseModel
    }})
async def import_issuer(json_file: UploadFile = File(...)):
  """Create issuer from json file

  Args:
    json_file (UploadFile): Upload json file consisting of issuer.
    json_schema should match Issuer

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
      IssuerImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=IssuerModel,
        model_obj=Issuer,
        object_name="issuers")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

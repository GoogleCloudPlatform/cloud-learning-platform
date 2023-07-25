"""
  Prior Experience endpoints
"""
from fastapi import APIRouter, UploadFile, File,Query
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models.prior_learning_assessment import PriorExperience
from schemas.prior_experience_schema import (GetPriorExperienceResponseModel,
        AllPriorExperienceResponseModel, PostPriorExperienceResponseModel,
        PriorExperienceModel, UpdatePriorExperienceResponseModel,
        UpdatePriorExperienceModel, DeletePriorExperienceModel,
        PriorExperienceImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except

router = APIRouter(
    tags=["Prior Experience"],
    responses=ERROR_RESPONSES)


@router.get(
    "/prior-experiences",
    response_model=AllPriorExperienceResponseModel,
    name="Get all Prior Experiences")
def get_prior_experiences(skip: int = Query(0, ge=0, le=2000),
                              limit: int = Query(10, ge=1, le=10)):
  """
  The get prior-experiences endpoint will return an array PriorExperiences from
  firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of prior-experiences array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllPriorExperienceResponseModel: Array of PriorExperience Object
  """
  try:
    collection_manager = PriorExperience.collection
    prior_experiences = collection_manager.order("-created_time").offset(
      skip).fetch(limit)
    prior_experiences = [
      i.get_fields(reformat_datetime=True) for i in prior_experiences
    ]
    count = 10000
    response = {"records": prior_experiences, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the prior experiences",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/prior-experience/{uuid}",
    response_model=GetPriorExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_prior_experience(uuid: str):
  """
  The get PriorExperience endpoint will return the PriorExperience
  from firestore of which uuid is provided.

  Args:
      uuid (str): Unique identifier for PriorExperience

  Raises:
      ResourceNotFoundException: If the PriorExperience does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetPriorExperienceResponseModel: PriorExperience Object
  """
  try:
    prior_experience = PriorExperience.find_by_uuid(uuid)
    prior_experience_fields = prior_experience.get_fields(
      reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the prior experience",
        "data": prior_experience_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/prior-experience",
    response_model=PostPriorExperienceResponseModel)
def create_prior_experience(input_prior_experience: PriorExperienceModel):
  """
  The post PriorExperience endpoint will add the given Prior Experience
  in request body to the firestore

  Args:
    input_skill (PriorExperienceModel): input prior experience to be inserted

  Raises:
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    PostPriorExperienceResponseModel: PriorExperience Object
  """
  try:
    input_prior_experience_dict = {**input_prior_experience.dict()}

    new_prior_experience = PriorExperience()
    new_prior_experience = new_prior_experience.from_dict(
      input_prior_experience_dict)
    new_prior_experience.uuid = ""
    new_prior_experience.save()
    new_prior_experience.uuid = new_prior_experience.id
    new_prior_experience.update()

    prior_experience_fields = new_prior_experience.get_fields(
      reformat_datetime=True)
    return {
      "success": True,
      "message": "Successfully created the prior experience",
      "data": prior_experience_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/prior-experience/{uuid}",
    response_model=UpdatePriorExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_prior_experience(uuid: str,
                            input_prior_experience: UpdatePriorExperienceModel):
  """
  Updates an prior experience

  Args:
    input_prior_experience (UpdatePriorExperienceModel): Required body of the
      prior experience

  Raises:
    ResourceNotFoundException: If the prior experience does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    UpdatePriorExperienceResponseModel: PriorExperience Object
  """
  try:
    existing_prior_experience = PriorExperience.find_by_uuid(uuid)

    input_prior_experience_dict = {
      **input_prior_experience.dict(exclude_unset=True)
    }
    prior_experience_fields = existing_prior_experience.get_fields()

    for key, value in input_prior_experience_dict.items():
      prior_experience_fields[key] = value
    for key, value in prior_experience_fields.items():
      setattr(existing_prior_experience, key, value)

    existing_prior_experience.update()
    prior_experience_fields = existing_prior_experience.get_fields(
      reformat_datetime=True)

    return {
      "success": True,
      "message": "Successfully updated the prior experience",
      "data": prior_experience_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/prior-experience/{uuid}",
    response_model=DeletePriorExperienceModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_prior_experience(uuid: str):
  """
  Delete an prior experience with the given uuid from firestore

  Args:
    uuid (str): Unique id of the prior experience

  Raises:
    ResourceNotFoundException: If the prior experience does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    JSON: Success/Fail Message
  """
  try:
    prior_experience = PriorExperience.find_by_uuid(uuid)
    PriorExperience.collection.delete(prior_experience.key)
    return {
      "success": True,
      "message": "Successfully deleted the prior experience"
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/prior-experience/import/json",
    response_model=PriorExperienceImportJsonResponse,
    responses={413: {
      "model": PayloadTooLargeResponseModel
    }},
    name="Import Prior Experiences from JSON file")
async def import_prior_experience(json_file: UploadFile = File(...)):
  """
  Create Prior Experience(s) from json file

  Args:
    json_file (UploadFile): Upload json file consisting of Prior Experience(s).
    json_schema should match PriorExperienceModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    PriorExperienceImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
      json_file=json_file,
      json_schema=PriorExperienceModel,
      model_obj=PriorExperience,
      object_name="prior experiences")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


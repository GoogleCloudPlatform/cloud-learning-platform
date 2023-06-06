""" Rubric endpoints """
import json
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Query
from json.decoder import JSONDecodeError
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models import Rubric
from services.rubric import create_rubric
from schemas.rubric_schema import (RubricModel, RubricModelResponse,
                                   UpdateRubricModel, DeleteRubric,
                                   RubricSearchModelResponse,
                                   AllRubricsModelResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["Rubric"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except


@router.get("/rubric/search", response_model=RubricSearchModelResponse)
def search_rubric(name: Optional[str] = None):
  """Search for rubric item based on the name

  Args:
      name(str): Name of the rubric. Defaults to None.

  Returns:
      RubricSearchModelResponse: List of rubric objects
  """
  try:
    result = []
    if name:
      # fetch rubric item that matches name
      name_node_items = Rubric.find_by_name(name)
      if name_node_items:
        result = [
            name_node_item.get_fields(reformat_datetime=True)
            for name_node_item in name_node_items
        ]
    else:
      raise ValidationError("Missing or invalid request parameters")

    return {
        "success": True,
        "message": "Successfully fetched the rubrics",
        "data": result
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get("/rubrics", response_model=AllRubricsModelResponse)
def get_rubrics(skip: int = Query(0, ge=0, le=2000),
                 limit: int = Query(10, ge=1, le=100)):
  """The get rubrics endpoint will return an array rubrics from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of rubric array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllRubricsModelResponse: Array of Rubric Object
  """
  try:
    rubrics = Rubric.collection.order("-created_time").offset(skip).fetch(limit)
    rubrics = [i.get_fields(reformat_datetime=True) for i in rubrics]
    count = 10000
    response = {"records": rubrics, "total_count": count}
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
    "/rubric/{uuid}",
    response_model=RubricModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_rubric(uuid: str):
  """The get rubric endpoint will return the rubric from firestore of which
  uuid is provided

  Args:
      uuid (str): Unique identifier for rubric

  Raises:
      ResourceNotFoundException: If the rubric does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      RubricModel: Rubric Object
  """
  try:
    rubric = Rubric.find_by_uuid(uuid)
    rubric_fields = rubric.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the rubric",
        "data": rubric_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/rubric", response_model=RubricModelResponse)
def create_rubrics(input_rubric: RubricModel):
  """The create rubric endpoint will add the rubric to the firestore if it
  does not exist.If the rubric exist then it will update the rubric

  Args:
      input_rubric (RubricModel): input rubric to be
      inserted

  Raises:
      ResourceNotFoundException: If the rubric does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      str: UUID(Unique identifier for rubric)
  """
  try:

    rubric_result = create_rubric(input_rubric)
    return rubric_result

  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.put(
    "/rubric",
    response_model=RubricModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_rubric(input_rubric: UpdateRubricModel):
  """Update a rubric

  Args:
      input_rubric (RubricModel): Required body of the rubric

  Raises:
      ResourceNotFoundException: If the rubric does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    existing_rubric = Rubric.find_by_uuid(input_rubric.uuid)

    input_rubric_dict = {**input_rubric.dict()}
    rubric_fields = existing_rubric.get_fields()

    for key, value in input_rubric_dict.items():
      rubric_fields[key] = value
    for key, value in rubric_fields.items():
      setattr(existing_rubric, key, value)

    existing_rubric.update()
    rubric_fields = existing_rubric.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the rubric",
        "data": rubric_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/rubric/{uuid}",
    response_model=DeleteRubric,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_rubric(uuid: str):
  """Delete a rubric from firestore

  Args:
      uuid (str): Unique id of the rubric

  Raises:
      ResourceNotFoundException: If the rubric does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    rubric = Rubric.find_by_uuid(uuid)
    Rubric.collection.delete(rubric.key)
    return {"success": True, "message": "Successfully deleted the Rubric"}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/rubric/import/json",
    response_model=List[str],
    responses={
        404: {
            "model": NotFoundErrorResponseModel
        },
        413: {
            "model": PayloadTooLargeResponseModel
        }
    })
async def import_rubrics(json_file: UploadFile = File(...)):
  """Create rubrics from json file

  Args:
    json_file (UploadFile): Upload json file consisting of rubrics.
    json_schema should match RubricModel

  Raises:
    Exception: 500 Internal Server Error if something fails
  """
  try:
    if not json_file.filename.endswith(".json"):
      raise ValidationError("Valid JSON file type is supported")
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
          f"File size is too large: {json_file.filename}")
    await json_file.seek(0)
    rubrics = json.load(json_file.file)
    inserted_data = []
    for rubric in rubrics:
      new_rubric = Rubric()
      new_rubric = new_rubric.from_dict(rubric)
      new_rubric.uuid = ""
      new_rubric.save()
      new_rubric.uuid = new_rubric.id
      new_rubric.update()
      inserted_data.append(new_rubric.uuid)
    return inserted_data
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except JSONDecodeError as e:
    raise BadRequest("Provided JSON is invalid") from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

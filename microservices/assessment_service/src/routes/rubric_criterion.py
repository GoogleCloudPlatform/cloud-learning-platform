""" RubricCriterion endpoints """
import json
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Query
from json.decoder import JSONDecodeError
from common.models import RubricCriterion
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from services.rubric_criteria import create_rubric_criterion
from schemas.rubric_criterion_schema import (RubricCriterionModel,
                                             RubricCriterionModelResponse,
                                             UpdateRubricCriterionModel,
                                             DeleteRubricCriterion,
                                             RubricCriterionSearchModelResponse,
                                             AllRubricCriterionsModelResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["RubricCriterion"], responses=ERROR_RESPONSES)

# pylint: disable = broad-except


@router.get(
    "/rubric-criterion/search",
    response_model=RubricCriterionSearchModelResponse)
def search_rubric_criterion(name: Optional[str] = None):
  """Search for rubric criterion item based on the name

  Args:
    name(str): Name of the rubric criterion. Defaults to None.

  Returns:
      RubricCriterionSearchModelResponse: List of rubric criterion objects
  """
  try:
    result = []
    if name:
      # fetch rubric criterion item that matches name
      name_node_items = RubricCriterion.find_by_name(name)
      if name_node_items:
        result = [
            name_node_item.get_fields(reformat_datetime=True)
            for name_node_item in name_node_items
        ]
    else:
      raise ValidationError("Missing or invalid request parameters")

    return {
        "success": True,
        "message": "Successfully fetched the rubric criterions",
        "data": result
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/rubric-criterions", response_model=AllRubricCriterionsModelResponse)
def get_rubric_criterions(skip: int = Query(0, ge=0, le=2000),
                           limit: int = Query(10, ge=1, le=100)):
  """The get rubric criterions endpoint will return an array rubric criterions
  from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of rubric criterion array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllRubricCriterionsModelResponse: Array of Rubric Criterion Object
  """
  try:
    rubric_criterions = RubricCriterion.collection.order(
        "-created_time").offset(skip).fetch(limit)
    rubric_criterions = [
        i.get_fields(reformat_datetime=True) for i in rubric_criterions
    ]
    count = 10000
    response = {"records": rubric_criterions, "total_count": count}
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
    "/rubric-criterion/{uuid}",
    response_model=RubricCriterionModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_rubric_criterion(uuid: str):
  """The get rubric_criterion endpoint will return the rubric criterion from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for rubric_criterion

  Raises:
      ResourceNotFoundException: If the rubric criterion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      RubricCriterionModel: RubricCriterion Object
  """
  try:
    rubric_criterion = RubricCriterion.find_by_uuid(uuid)
    rubric_criterion_fields = rubric_criterion.get_fields(
        reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the rubric criterion",
        "data": rubric_criterion_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/rubric-criterion", response_model=RubricCriterionModelResponse)
def create_rubric_criteria(input_rubric_criterion: RubricCriterionModel):
  """The create rubric criterion endpoint will add the rubric criterion to the
  firestore if it does not exist.If the rubric criterion exist then it will
  update the rubric criterion

  Args:
      input_rubric_criterion (RubricCriterionModel): input rubric criterion to
      be inserted

  Raises:
      ResourceNotFoundException: If the rubric criterion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      str: UUID(Unique identifier for rubric criterion)
  """
  try:

    rubric_criteria_result = create_rubric_criterion(input_rubric_criterion)
    return rubric_criteria_result

  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/rubric-criterion",
    response_model=RubricCriterionModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_rubric_criterion(input_rubric_criterion: UpdateRubricCriterionModel):
  """Update a rubric criterion

  Args:
      input_rubric_criterion (RubricCriterionModel): Required body of the
      rubric criterion

  Raises:
      ResourceNotFoundException: If the rubric criterion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    existing_rubric_criterion = RubricCriterion.find_by_uuid(
        input_rubric_criterion.uuid)

    input_rubric_criterion_dict = {**input_rubric_criterion.dict()}
    rubric_criterion_fields = existing_rubric_criterion.get_fields()

    for key, value in input_rubric_criterion_dict.items():
      rubric_criterion_fields[key] = value
    for key, value in rubric_criterion_fields.items():
      setattr(existing_rubric_criterion, key, value)

    existing_rubric_criterion.update()
    rubric_criterion_fields = existing_rubric_criterion.get_fields(
        reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the rubric criterion",
        "data": rubric_criterion_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/rubric-criterion/{uuid}",
    response_model=DeleteRubricCriterion,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_rubric_criterion(uuid: str):
  """Delete a rubric_criterion from firestore

  Args:
      uuid (str): Unique id of the rubric criterion

  Raises:
      ResourceNotFoundException: If the rubric criterion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    rubric_criterion = RubricCriterion.find_by_uuid(uuid)
    RubricCriterion.collection.delete(rubric_criterion.key)
    return {
        "success": True,
        "message": "Successfully deleted the Rubric Criterion"
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/rubric-criterion/import/json",
    response_model=List[str],
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_rubric_criterions(json_file: UploadFile = File(...)):
  """Create rubric_criterions from json file

  Args:
    json_file (UploadFile): Upload json file consisting of rubric_criterions.
    json_schema should match RubricCriterionModel

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
    rubric_criterions = json.load(json_file.file)
    inserted_data = []
    for rubric_criterion in rubric_criterions:
      new_rubric_criterion = RubricCriterion()
      new_rubric_criterion = new_rubric_criterion.from_dict(rubric_criterion)
      new_rubric_criterion.uuid = ""
      new_rubric_criterion.save()
      new_rubric_criterion.uuid = new_rubric_criterion.id
      new_rubric_criterion.update()
      inserted_data.append(new_rubric_criterion.uuid)
    return inserted_data
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except JSONDecodeError as e:
    raise BadRequest("Provided JSON is invalid") from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

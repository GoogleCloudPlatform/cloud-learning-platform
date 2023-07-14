"""
  Approved Experience endpoints
"""
import re
import traceback
from typing import Union, List, Optional
from typing_extensions import Literal
from fastapi import APIRouter, UploadFile, File, Query
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models.prior_learning_assessment import ApprovedExperience
from schemas.approved_experience_schema import \
  (GetApprovedExperienceResponseModel,
  AllApprovedExperienceResponseModel, PostApprovedExperienceResponseModel,
  ApprovedExperienceModel, UpdateApprovedExperienceResponseModel,
  UpdateApprovedExperienceModel, DeleteApprovedExperienceModel,
  ApprovedExperienceImportJsonResponse,AllApprovedOrganisationResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES
# pylint: disable = broad-except,redefined-builtin

router = APIRouter(
    tags=["Approved Experience"],
    responses=ERROR_RESPONSES)


@router.get(
    "/approved-experience/search",
    response_model=AllApprovedExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def approved_exp_keyword_search(
    keyword: str,
    skip: int = Query(0, ge=0, le=2000),
    limit: int = Query(6, ge=1, le=100),
    type: Union[List[str], None] = Query(default=None),
    student_type: Union[List[str], None] = Query(default=None),
    class_level: Union[List[str], None] = Query(default=None),
    status: Union[List[str], None] = Query(default=None),
    organization: Union[List[str], None] = Query(default=None),
    credits_range_lower_limit: Optional[int] = None,
    credits_range_upper_limit: Optional[int] = None,
    sort_by:
      Optional[Literal["total_credit", "experience_name"]] = "total_credit",
    sort_order: Optional[Literal["ascending", "descending"]] = "descending",
  ):
  """
  Search for approved experience title and description
  using the provided keyword
  Args:
    keyword (str): Required text for search
    skip (int): Number of objects to be skipped
    limit (int): Size of skill array to be returned
    type (list): type to filter approved_experiences
    student_type (list): student_type to filter approved_experiences
    class_level (list): class_level to filter approved_experiences
    status (list): status to filter approved_experiences
    organizations (list): organizations to filter approved_experiences
    credits_range_lower_limit (int):
        lower limit of credits to filter approved_experiences
    credits_range_upper_limit (int):
        upper limit of credits to filter approved_experiences
    sort_by (str): field on which sorting would be performed. Values can be
        total_credit or experience_name. Default is total_credit.
    sort_order (str): sorting order for the sort_by field. Default is
        descending.
  Returns:
    AllApprovedExperienceResponseModel : Array of matched Keywords Object
  """
  try:
    keyword = re.escape(keyword)
    collection_manager = ApprovedExperience.collection
    if type is not None:
      collection_manager = collection_manager.filter("type", "in", type)
    if student_type is not None:
      collection_manager = collection_manager.filter("student_type", "in",
                                                     student_type)
    if class_level is not None:
      collection_manager = collection_manager.filter("class_level", "in",
                                                     class_level)
    if status is not None:
      collection_manager = collection_manager.filter("status", "in", status)

    ae_docs = list(collection_manager.fetch())
    ae_dicts = [doc.get_fields(reformat_datetime=True) for doc in ae_docs]
    if organization is not None:
      ae_dicts = [doc for doc in ae_dicts \
        if doc.get("organization", None) in organization]
    if credits_range_lower_limit is not None:
      ae_dicts = [doc for doc in ae_dicts \
        if doc.get("credits_range", {}).get("lower_limit", None) and \
          doc["credits_range"]["lower_limit"] >= credits_range_lower_limit]
    if credits_range_upper_limit is not None:
      ae_dicts = [doc for doc in ae_dicts \
        if doc.get("credits_range", {}).get("upper_limit", None) and \
          doc["credits_range"]["upper_limit"] <= credits_range_upper_limit]
    search_result = []
    for doc in ae_dicts:
      if doc.get("description", None) and \
          len(re.findall(keyword.lower(), doc["description"].lower())) > 0:
        search_result.append(doc)
      elif doc.get("title", None) and \
          len(re.findall(keyword.lower(), doc["title"].lower())) > 0:
        search_result.append(doc)

    if sort_by == "total_credit" and sort_order == "descending":
      search_result = sorted(search_result,
        key=lambda d: d["credits_range"]["upper_limit"], reverse=True)
    elif sort_by == "total_credit" and sort_order == "ascending":
      search_result = sorted(search_result,
        key=lambda d: d["credits_range"]["upper_limit"])
    elif sort_by == "experience_name" and sort_order == "descending":
      search_result = sorted(search_result,
        key=lambda d: d["title"], reverse=True)
    elif sort_by == "experience_name" and sort_order == "ascending":
      search_result = sorted(search_result, key=lambda d: d["title"])

    count = len(search_result)
    response = {"records": search_result[skip:skip+limit], "total_count": count}

    return {
      "success": True,
      "message": "Successfully fetched the Approved Experiences",
      "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/approved-experiences",
    response_model=AllApprovedExperienceResponseModel,
    name="Get all Approved Experiences")
def get_approved_experiences(skip: int = Query(0, ge=0, le=2000),
                              limit: int = Query(10, ge=1, le=10)):
  """
  The get approved-experiences endpoint will return an array ApprovedExperiences
  from firestore

  Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of approved-experiences array to be returned

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllApprovedExperienceResponseModel: Array of ApprovedExperience Object
  """
  try:
    collection_manager = ApprovedExperience.collection
    approved_experiences = collection_manager.order("-created_time").offset(
      skip).fetch(limit)
    approved_experiences = [
      i.get_fields(reformat_datetime=True) for i in approved_experiences
    ]
    count = 10000
    response = {"records": approved_experiences, "total_count": count}
    return {
        "success": True,
        "message": "Successfully fetched the approved experiences",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/approved-experience/{uuid}",
    response_model=GetApprovedExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_approved_experience(uuid: str):
  """
  The get ApprovedExperience endpoint will return the ApprovedExperience
  from firestore of which uuid is provided.

  Args:
      uuid (str): Unique identifier for ApprovedExperience

  Raises:
      ResourceNotFoundException: If the ApprovedExperience does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetApprovedExperienceResponseModel: ApprovedExperience Object
  """
  try:
    approved_experience = ApprovedExperience.find_by_uuid(uuid)
    approved_experience_fields = approved_experience.get_fields(
      reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully fetched the approved experience",
        "data": approved_experience_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/approved-experience",
    response_model=PostApprovedExperienceResponseModel)
def create_approved_experience(input_approved_experience:\
                                  ApprovedExperienceModel):
  """
  The post ApprovedExperience endpoint will add the given Approved Experience
  in request body to the firestore

  Args:
    input_skill (ApprovedExperienceModel): input approved experience
    to be inserted

  Raises:
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    PostApprovedExperienceResponseModel: ApprovedExperience Object
  """
  try:
    input_approved_experience_dict = {**input_approved_experience.dict()}

    new_approved_experience = ApprovedExperience()
    new_approved_experience = new_approved_experience.from_dict(
      input_approved_experience_dict)
    new_approved_experience.uuid = ""
    new_approved_experience.save()
    new_approved_experience.uuid = new_approved_experience.id
    new_approved_experience.update()

    approved_experience_fields = new_approved_experience.get_fields(
      reformat_datetime=True)
    return {
      "success": True,
      "message": "Successfully created the approved experience",
      "data": approved_experience_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/approved-experience/{uuid}",
    response_model=UpdateApprovedExperienceResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_approved_experience(uuid: str,input_approved_experience:\
                                          UpdateApprovedExperienceModel):
  """
  Updates an approved experience

  Args:
    input_approved_experience (UpdateApprovedExperienceModel): Required body of
    the approved experience

  Raises:
    ResourceNotFoundException: If the approved experience does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    UpdateApprovedExperienceResponseModel: ApprovedExperience Object
  """
  try:
    existing_approved_experience = ApprovedExperience.find_by_uuid(uuid)

    input_approved_experience_dict = {
      **input_approved_experience.dict(exclude_unset=True)
    }
    approved_experience_fields = existing_approved_experience.get_fields()

    for key, value in input_approved_experience_dict.items():
      approved_experience_fields[key] = value
    for key, value in approved_experience_fields.items():
      setattr(existing_approved_experience, key, value)

    existing_approved_experience.update()
    approved_experience_fields = existing_approved_experience.get_fields(
      reformat_datetime=True)

    return {
      "success": True,
      "message": "Successfully updated the approved experience",
      "data": approved_experience_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/approved-experience/{uuid}",
    response_model=DeleteApprovedExperienceModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_approved_experience(uuid: str):
  """
  Delete an approved experience with the given uuid from firestore

  Args:
    uuid (str): Unique id of the approved experience

  Raises:
    ResourceNotFoundException: If the approved experience does not exist
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    JSON: Success/Fail Message
  """
  try:
    approved_experience = ApprovedExperience.find_by_uuid(uuid)
    ApprovedExperience.collection.delete(approved_experience.key)
    return {
      "success": True,
      "message": "Successfully deleted the approved experience"
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/approved-experience/import/json",
    response_model=ApprovedExperienceImportJsonResponse,
    responses={413: {
      "model": PayloadTooLargeResponseModel
    }},
    name="Import Approved Experiences from JSON file")
async def import_approved_experience(json_file: UploadFile = File(...)):
  """
  Create Approved Experience(s) from json file

  Args:
    json_file (UploadFile): Upload json file consisting of Approved_Experiences
    json_schema should match ApprovedExperienceModel

  Raises:
    Exception: 500 Internal Server Error if something fails

  Returns:
    ApprovedExperienceImportJsonResponse: Array of uuid's
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
      json_file=json_file,
      json_schema=ApprovedExperienceModel,
      model_obj=ApprovedExperience,
      object_name="approved experiences")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/approved-experience/organisations/unique",
    response_model=AllApprovedOrganisationResponseModel,
    name="Get all Approved Organisations")
def get_approved_organisations():
  """
  The get approved-organisations endpoint will return an array ApprovedOrgs
  from firestore collection of ApprovedExperiences

  Args:
      No args as we need to fetch all orgs

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllApprovedOrganisationResponseModel: List of unique organisations fetched
      from firestore collection
  """
  try:
    collection_manager = ApprovedExperience.collection
    approved_experiences = collection_manager.fetch()

    org_list = list({doc.organization for doc in approved_experiences})
    return {
        "success": True,
        "message": \
          "Successfully fetched the unique list of approved organisations",
        "data": org_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

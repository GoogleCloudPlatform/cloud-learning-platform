"""
  PLA Records endpoints
"""
import re
import traceback
from fastapi import APIRouter, UploadFile, File, Query
from typing import Optional,Union, List
from typing_extensions import Literal
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, PayloadTooLarge)
from common.models import (PLARecord, PriorExperience, ApprovedExperience)
from schemas.pla_record_schema import (BasicPLARecordModel,PLARecordModel,
        UpdatePLARecordModel,GetPLARecordModelResponse,
        PostPLARecordModelResponse,UpdatePLARecordModelResponse,
        AllPLARecordModelResponse,DeletePLARecordModelResponse,
        PLARecordSearchModelResponse,PLARecordImportJsonResponse,
        AllAssessorsResponseModel, UpdatePLARecordExperienceModel,
        GetPLAReportResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(
    tags=["PLA Record"],
    responses=ERROR_RESPONSES)

@router.get(
    "/pla-records",
    response_model=AllPLARecordModelResponse,
    name="Get all PLA Records")
def get_all_pla_records(skip: int = Query(0, ge=0, le=2000),
                          limit: int = Query(10, ge=1, le=10)):
  """
  Returns an array of PLARecords from firestore
  Args:
    skip (int): Number of objects to be skipped
    limit (int): Size of PLA Records array to be returned
  Raises:
    Exception: 500 Internal Server Error if something went wrong
  Returns:
    AllPLARecordModelResponse: Array of PLARecord objects
  """
  try:
    pla_records = PLARecord.collection.order("-created_time").offset(
      skip).fetch(limit)
    pla_records = [
      i.get_fields(reformat_datetime=True) for i in pla_records
    ]
    count = 10000
    response = {"records": pla_records, "total_count": count}
    return {
      "success": True,
      "message": "Successfully fetched the PLA Records",
      "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.get(
    "/pla-record/search", response_model=PLARecordSearchModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def search_pla_record(
  skip: int = Query(0, ge=0, le=2000),
  limit: int = Query(6, ge=1, le=100),
  keyword: Optional[str] = None,
  start_date: Optional[str] = None,
  end_date: Optional[str] = None,
  status: Union[List[str], None] = Query(default=None),
  assessor: Union[List[str], None] = Query(default=None),
  sort_by:
      Optional[Literal["title", "date_last_edited", "ID Number"]] = "title",
  sort_order: Optional[Literal["ascending", "descending"]] = "ascending",
  ):
  """
  Search for pla records/sessions title and description using the provided
  keyword. If keyword is not passed, it will return all the records.
  Args:
    skip (int): Number of objects to be skipped
    limit (int): Size of skill array to be returned
    keyword (str): Text for search
    status (list): status to filter pla_records
    assessor_name (list): assessors to filter pla_records
    start_date (str): lower limit og save date to filter pla_records
    end_date (str): lower limit og save date to filter pla_records
    sort_by (str): field on which sorting would be performed. Values can be
        title or date_last_edited ot ID Number. Default is title.
    sort_order (str): sorting order for the sort_by field. Default is
        ascending.
  Returns:
    PLARecordSearchModelResponse : Array of matched Keywords Object along
    with the count of the total search results
  """
  try:
    collection_manager = PLARecord.collection.filter("type", "==", "saved")
    if assessor is not None:
      collection_manager = collection_manager.filter("assessor_name", "in",
                                                     assessor)
    pla_docs = list(collection_manager.fetch())
    pla_dicts = [doc.get_fields(reformat_datetime=True) for doc in pla_docs]
    if start_date is not None:
      pla_dicts = [doc for doc in pla_dicts \
        if doc.get("last_modified_time", None) and \
          doc.get("last_modified_time", None) >= start_date]
    if end_date is not None:
      pla_dicts = [doc for doc in pla_dicts \
        if doc.get("last_modified_time", None) and \
          doc.get("last_modified_time", None) <= end_date]
    if status is not None:
      pla_dicts_status = []
      pla_dicts_flagged = []
      pla_dicts_archived = []
      if "Archived" in status:
        pla_dicts_archived = [doc for doc in pla_dicts \
                              if doc.get("is_archived")]
        status.remove("Archived")
      if "Flagged" in status:
        pla_dicts_flagged = [doc for doc in pla_dicts if doc.get("is_flagged") \
                             if not doc.get("is_archived")]
        status.remove("Flagged")
      if status is not None:
        pla_dicts_status = [doc for doc in pla_dicts \
                            if doc.get("status", None) in status
                            if not doc.get("is_archived")
                            if not doc.get("is_flagged")]
      pla_dicts = pla_dicts_flagged + pla_dicts_archived + pla_dicts_status

    if keyword is not None:
      search_result = []
      keyword = re.escape(keyword)
      for doc in pla_dicts:
        if doc.get("description", None) and \
            len(re.findall(keyword.lower(), doc["description"].lower())) > 0:
          search_result.append(doc)
        elif doc.get("title", None) and \
            len(re.findall(keyword.lower(), doc["title"].lower())) > 0:
          search_result.append(doc)
    else:
      search_result = pla_dicts

    if sort_by == "title" and sort_order == "descending":
      search_result = sorted(search_result,
        key=lambda d: d["title"], reverse=True)
    elif sort_by == "title" and sort_order == "ascending":
      search_result = sorted(search_result,
        key=lambda d: d["title"])
    elif sort_by == "ID Number" and sort_order == "descending":
      search_result = sorted(search_result,
        key=lambda d: d["id_number"], reverse=True)
    elif sort_by == "ID Number" and sort_order == "ascending":
      search_result = sorted(search_result, key=lambda d: d["id_number"])
    elif sort_by == "date_last_edited" and sort_order == "descending":
      search_result = sorted(search_result, key=\
                             lambda d: d["last_modified_time"],reverse=True)
    elif sort_by == "date_last_edited" and sort_order == "ascending":
      search_result = sorted(search_result, key=\
                             lambda d: d["last_modified_time"])

    count = len(search_result)
    response = {"records": search_result[skip:skip+limit], "total_count": count}

    return {
      "success": True,
      "message": "Successfully fetched the PLA Records",
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
    "/pla-record/{uuid}",
    response_model=GetPLARecordModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_pla_record(uuid: str):
  """The get pla record endpoint will return the pla record from
  firestore of which uuid is provided

  ### Args:
  uuid: `str`
    Unique identifier for pla record
  ### Raises:
  ResourceNotFoundException:
    If the pla record does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong

  ### Returns:
  PLA Record: `GetPLARecordModelResponse`
  """
  try:
    pla_record = PLARecord.find_by_uuid(uuid)
    pla_record = pla_record.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the PLA Record",
        "data": pla_record
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.get(
    "/pla-record/user/{user_id}",
    response_model=GetPLARecordModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_draft_pla_record_for_user(user_id: str,
                                  fetch_tree: Optional[bool] = False):
  """The get pla record endpoint will return the pla record from
  firestore for the specific user_id

  ### Args:
  user_id: `str`
    Unique identifier for user
  fetch_tree: `bool`
    if True, replaces the prior experience and approved experience UUIDs with
    their documents in the response body. If False, the experience UUIDs are
    not replaced. Default value is False.
  ### Raises:
  ResourceNotFoundException:
    If the pla record does not exist <br/>
  Exception 500:
    Internal Server Error if something went wrong

  ### Returns:
  PLA Record: `GetPLARecordModelResponse`
  """
  try:
    pla_record = PLARecord.find_by_user_id(user_id)
    pla_record_dict = pla_record.get_fields(reformat_datetime=True)
    if fetch_tree:
      prior_experiences = []
      approved_experiences = []
      for pe_uuid in pla_record_dict["prior_experiences"]:
        prior_experience = PriorExperience.find_by_uuid(pe_uuid)
        prior_experience_dict = prior_experience.get_fields(
          reformat_datetime=True)
        prior_experiences.append(prior_experience_dict)
      for ae_uuid in pla_record_dict["approved_experiences"]:
        approved_experience = ApprovedExperience.find_by_uuid(ae_uuid)
        approved_experience_dict = approved_experience.get_fields(
          reformat_datetime=True)
        approved_experiences.append(approved_experience_dict)
      pla_record_dict["prior_experiences"] = prior_experiences
      pla_record_dict["approved_experiences"] = approved_experiences
    return {
        "success": True,
        "message": "Successfully fetched the pla record",
        "data": pla_record_dict
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/pla-record/{uuid}/report",
    response_model=GetPLAReportResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_pla_record_report(uuid: str):
  """
  Method to generate PLARecord/session report.

  Args:
    uuid (str): uuid of the PLARecord for which the report has to be generated.

  Returns:
    GetPLAReportResponseModel: All the fields for the PLARecord/session report.
  """
  try:
    pla_record = PLARecord.find_by_uuid(uuid)
    pla_record_dict = pla_record.get_fields(reformat_datetime=True)
    # generating report
    pla_record_dict["experiences_found"] = len(
      pla_record_dict["prior_experiences"] + \
      pla_record_dict["approved_experiences"])
    pla_record_dict["experiences_matched"] = len(
      pla_record_dict["approved_experiences"])
    pla_record_dict["progress"] = (pla_record_dict[
      "experiences_matched"]/pla_record_dict["experiences_found"])*100
    potential_credits = 0
    approved_experiences = []
    prior_experiences = []
    for ap_uuid in pla_record_dict["approved_experiences"]:
      ap = ApprovedExperience.find_by_uuid(ap_uuid)
      ap = ap.get_fields(reformat_datetime=True)
      approved_experiences.append(ap)
      potential_credits += ap["credits_range"]["lower_limit"]
    pla_record_dict["potential_credits"] = potential_credits
    pla_record_dict["experiences"] = {}
    for pe_uuid in pla_record_dict["prior_experiences"]:
      pe = PriorExperience.find_by_uuid(pe_uuid)
      pe = pe.get_fields(reformat_datetime=True)
      prior_experiences.append(pe)
    pla_record_dict["experiences"]["experiences_with_matches"] = \
      approved_experiences
    pla_record_dict["experiences"]["experiences_without_matches"] = \
      prior_experiences

    setattr(pla_record, "progress", pla_record_dict["progress"])
    pla_record.update()

    return {
      "success": True,
      "message": "Successfully generated the PLA Record report",
      "data": pla_record_dict
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/pla-record",
    response_model=PostPLARecordModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_pla_record(input_pla_record: PLARecordModel):
  """
  The create pla record endpoint will add the given pla record in
  request body to the firestore

  Args:
      input_pla_record (PLARecordModel): input pla record to be inserted

  Raises:
      ResourceNotFoundException: If the pla record does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      PostPLARecordModelResponse: PLA Record Object
  """
  try:
    new_pla_record = PLARecord()
    input_pla_record_dict = {**input_pla_record.dict()}
    for pe_uuid in input_pla_record_dict["prior_experiences"]:
      PriorExperience.find_by_uuid(pe_uuid)
    for ae_uuid in input_pla_record_dict["approved_experiences"]:
      ApprovedExperience.find_by_uuid(ae_uuid)
    new_pla_record = new_pla_record.from_dict(
        input_pla_record_dict)
    new_pla_record.uuid = ""
    new_pla_record.save()

    new_pla_record.uuid = new_pla_record.id
    new_pla_record.id_number += len(list(PLARecord.collection.fetch()))-1
    if not input_pla_record_dict.get("title", None):
      new_pla_record.title = "Session #" + str(new_pla_record.id_number)
    new_pla_record.update()
    pla_record_fields = new_pla_record.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully created the PLA Record",
        "data": pla_record_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.put(
    "/pla-record/{uuid}",
    response_model=UpdatePLARecordModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_pla_record(
    uuid: str,
    input_pla_record: UpdatePLARecordModel):
  """Update the PLA Record with the uuid passed in the request body

  Args:
      input_pla_record (UpdatePLARecordModel): Required body of the
      PLA record

  Raises:
      ResourceNotFoundException: If the PLA record does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdatePLARecordModelResponse: PLA Record Object
  """
  try:
    input_pla_record_dict = {**input_pla_record.dict()}
    # Updating the original doc
    updated_doc_fields = \
        CommonAPIHandler.update_document(PLARecord,
                                         uuid,
                                         input_pla_record_dict)

    return {
        "success": True,
        "message": "Successfully updated the PLA Record",
        "data": updated_doc_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/pla-record/{uuid}/experience",
    response_model=UpdatePLARecordModelResponse)
def append_remove_experience_from_pla_record(uuid: str,
    input_dict: UpdatePLARecordExperienceModel,
    update_type: Optional[Literal["append", "remove"]] = "append"):
  """
  Method to append or remove the Prior Experience and/or Approved Experience
  UUIDs to/from the PLA_record with the given uuid.

  Args:
    uuid (str): uuid of the PLA_record that is to updated
    input_dict (UpdatePLARecordExperienceModel): Request body containing the
        Prior Experience and/or Approved Experience UUIDs that are to be
        appended/remove from the PLA_record
    update_type (str): "append" or "remove". append will add the UUID in the
        list, remove will remove the UUID from the list. Default is "append".

  Returns:
    UpdatePLARecordModelResponse: PLA Record Object
  """
  try:
    pla_record = PLARecord.find_by_uuid(uuid)
    pla_record_dict = pla_record.get_fields(reformat_datetime=True)

    input_pla_record_dict = {**input_dict.dict(exclude_unset=True)}

    prior_experiences = []
    approved_experiences = []
    if input_pla_record_dict.get("prior_experiences"):
      prior_experiences = input_pla_record_dict["prior_experiences"]
    if input_pla_record_dict.get("approved_experiences"):
      approved_experiences = input_pla_record_dict["approved_experiences"]

    if update_type == "append":
      for pe_uuid in prior_experiences:
        PriorExperience.find_by_uuid(pe_uuid)
      for ae_uuid in approved_experiences:
        ApprovedExperience.find_by_uuid(ae_uuid)
      pla_record_dict["prior_experiences"].extend(prior_experiences)
      pla_record_dict["approved_experiences"].extend(approved_experiences)
    elif update_type == "remove":
      pla_record_dict["prior_experiences"] = [i for i in \
        pla_record_dict["prior_experiences"] if i not in prior_experiences]
      pla_record_dict["approved_experiences"] = [i for i in \
        pla_record_dict["approved_experiences"] if \
        i not in approved_experiences]

    setattr(pla_record, "prior_experiences",
            pla_record_dict["prior_experiences"])
    setattr(pla_record, "approved_experiences",
            pla_record_dict["approved_experiences"])
    pla_record.update()

    return {
        "success": True,
        "message": "Successfully updated the PLA Record",
        "data": pla_record_dict
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/pla-record/{uuid}",
    response_model=DeletePLARecordModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_pla_record(uuid: str):
  """Delete the pla-record with the given uuid from firestore

  Args:
      uuid (str): Unique id of the PLA record

  Raises:
      ResourceNotFoundException: If the PLA record does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    pla_record = PLARecord.find_by_uuid(uuid)
    if pla_record.type == "draft":
      # delete all the added Prior Experiences
      # as the drawer contents are cleared
      for pe_uuid in pla_record.prior_experiences:
        prior_experience = PriorExperience.find_by_uuid(pe_uuid)
        PriorExperience.collection.delete(prior_experience.key)
    PLARecord.collection.delete(pla_record.key)
    return {
      "success": True,
      "message": "Successfully deleted the PLA Record"
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

@router.post(
    "/pla-record/import/json",
    response_model=PLARecordImportJsonResponse,
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }},
    name="Import PLA record from JSON file")
async def import_pla_records(json_file: UploadFile = File(...)):
  """Create PLA records from json file
  ### Args:
  json_file: `UploadFile`
    Upload json file consisting of PLA records.
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something fails
  ### Returns:
    PLA record UUID: `PLARecordImportJsonResponse`
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicPLARecordModel,
        model_obj=PLARecord,
        object_name="pla_records")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/pla-record/assessors/unique",
    response_model=AllAssessorsResponseModel,
    name="Get all Assessors Name")
def get_all_assessor_names():
  """
  This endpoint will return a list of all unique Assessors names in the
  PLARecord collection from the database.

  Args:
      None

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      AllAssessorsResponseModel: List of unique Assessors names fetched
      from firestore collection.
  """
  try:
    pla_records = PLARecord.collection.fetch()
    assessor_names = list({doc.assessor_name for doc in pla_records})
    return {
        "success": True,
        "message": "Successfully fetched the unique list of Assessor names",
        "data": assessor_names
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e

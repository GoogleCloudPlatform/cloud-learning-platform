"""
  Bulk Upload user events endpoints to the firestore collection
"""
import traceback
import pandas as pd
import time
from typing import List
from fastapi import APIRouter, UploadFile, File
from common.models import UserEvent
from common.utils.logging_handler import Logger
from common.utils.gcs_adapter import upload_file_to_bucket,write_csv_to_bucket
from common.utils.errors import ValidationError,ResourceNotFoundException
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                            ResourceNotFound)
from services.create_user_events import (create_user_event,
                                          create_synthetic_data)
from schemas.user_event_schema import (BulkUploadResponse,DeleteResponse,
                                        SyntheticDataCreate)
from config import (ALLOWED_FILE_TYPES, GCP_BUCKET,
                    ERROR_RESPONSES,REQUIRED_FIELDS)

router = APIRouter(
  tags=["User Events"],
  responses=ERROR_RESPONSES)

@router.post("/bulk-upload",
  response_model=BulkUploadResponse,
  name="Bulk Upload User Events")
async def bulk_upload(files: List[UploadFile] = File(...)):
  """
  API endpoint for uploading files with user events
  Args:
    files (List[UploadFile]): list of uploaded files. Files can be CSV only
  Raises:
    Exception: 500 Internal Server Error if something fails.
  Returns:
    BulkUploadResponse: Success message once processed successfully
  """
  try:
    gcs_file_paths = []
    #adding validations
    for file_ in files:
      if not file_.filename.endswith(tuple(ALLOWED_FILE_TYPES)):
        raise ValidationError(
        f"Invalid document type. Allowed types are: {ALLOWED_FILE_TYPES}")

    #uploading files
    for file_ in files:
      gcs_file_paths.append(upload_file_to_bucket(
        GCP_BUCKET, "mastery_model/user_events", file_.filename, file_.file))

    num_user_events = 0
    req_schema_list = list(REQUIRED_FIELDS.keys())
    for file_path in gcs_file_paths:
      data = pd.read_csv(file_path)
      columns_list = list(data.columns)
      for value in req_schema_list:
        if value not in columns_list:
          raise ValidationError(
          "Invalid document schema. Required fields are:"
          f"{req_schema_list}")

      for col in columns_list:
        if col not in req_schema_list:
          raise ValidationError(
            f"Invalid document schema. Field not allowed: {col}")

      num_user_events = num_user_events+ create_user_event(file_path)
      num_course_ids = list(data["course_id"].unique())

    print("Succesfully completed")
    return{
      "success": True,
      "message": "Successfully created the user events",
      "num_user_events": num_user_events,
      "course_ids": num_course_ids
    }

  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.delete("/delete",
  response_model=DeleteResponse,
  name="Delete User Events")
def delete_user_event(user_id: str=None,course_id: str=None):
  try:
    if user_id is None and course_id is None:
      raise ValidationError(
        "Please enter either user_id or course_id needed for deletion")
    elif user_id and course_id:
      collection_manager = UserEvent.collection.filter(
        "user_id", "==", user_id).filter(
          "course_id", "==", course_id)
    elif user_id and course_id is None:
      collection_manager = UserEvent.collection.filter(
        "user_id", "==", user_id)
    elif course_id and user_id is None:
      collection_manager = UserEvent.collection.filter(
        "course_id", "==", course_id)

    user_events = collection_manager.fetch()

    data = []
    for user_event in user_events:
      data.append(user_event.id)
      UserEvent.delete_by_id(user_event.id)

    if len(data) == 0:
      raise ResourceNotFoundException(
          "No such user event data found"
        )

    return{
      "success": True,
      "message": "Successfully deleted the user events",
      "deleted_user_events": data
    }

  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

@router.post("/create-synthetic-data",
  response_model=SyntheticDataCreate,
  name="Generate syntethic csv data")
def create_Synthetic_data(num: int):
  try:
    if num> 1000:
      raise ValidationError(
        "Please enter a number less than 1000 for creating synthetic_data")

    file_body = create_synthetic_data(num)
    ts=str(time.time()).split(".",maxsplit=1)[0]
    file_name = "synthetic_events"+ ts +".csv"
    prefix= "mastery_model/user_events_synthetic"
    gcs_uri= write_csv_to_bucket(GCP_BUCKET,prefix,file_name,file_body)

    return{
      "success": True,
      "message": "Successfully created the synthetic data in a csv",
      "gcs_path" : gcs_uri
    }

  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e







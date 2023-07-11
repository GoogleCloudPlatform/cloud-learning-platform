"""Upload transcripts endpoints"""
import traceback
from typing import List
from fastapi import APIRouter, UploadFile, File
from common.utils.gcs_adapter import upload_file_to_bucket
from common.utils.logging_handler import Logger
from common.utils.errors import ValidationError, PayloadTooLargeError
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          PayloadTooLarge)
from schemas.upload_schema import UploadResponseModel
from config import (ALLOWED_TRANSCRIPT_TYPES, GCP_BUCKET, PAYLOAD_FILE_SIZE,
                    ERROR_RESPONSES)
# pylint: disable = broad-except

router = APIRouter(
    tags=["Upload Transcripts"],
    responses=ERROR_RESPONSES)

@router.post("/upload",
  response_model=UploadResponseModel,
  name="Upload Transcripts")
async def upload_transcripts(files: List[UploadFile] = File(...)):
  """
  API endpoint for uploading transcripts.

  Args:
    files (List[UploadFile]): list of uploaded files. Files can be
    PDF, CSV, Doc, XLS, Zip, JPEG, etc.

  Raises:
    Exception: 500 Internal Server Error if something fails.

  Returns:
    UploadResponseModel: List of uploaded gcs file paths.
  """
  try:
    gcs_file_paths = []
    for file_ in files:
      if not file_.filename.endswith(tuple(ALLOWED_TRANSCRIPT_TYPES)):
        raise ValidationError(
        f"Invalid document type. Allowed types are: {ALLOWED_TRANSCRIPT_TYPES}")
      if len(await file_.read()) > PAYLOAD_FILE_SIZE:
        raise PayloadTooLargeError(
          f"File size is too large: {file_.filename}"
        )
      await file_.seek(0)
    for file_ in files:
      gcs_file_paths.append(upload_file_to_bucket(
        GCP_BUCKET, "pla/user-transcripts", file_.filename, file_.file))
    return {
      "success": True,
      "message": "Successfully uploaded the transcripts",
      "data": gcs_file_paths
    }
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e), data=e.data) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

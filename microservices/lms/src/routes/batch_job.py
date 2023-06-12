'''Batch Job Endpoint'''
from fastapi import APIRouter
from common.models import LmsJob
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import ResourceNotFound, InternalServerError, BadRequest
from schemas.lms_job import (LmsJobsListResponseModel,
                               LmsJobResponseModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)

router = APIRouter(
    prefix="/batch-jobs",
    tags=["Batch Jobs"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        404: {
            "model": NotFoundErrorResponseModel
        },
        409: {
            "model": ConflictResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.get("", response_model=LmsJobsListResponseModel)
def get_lms_jobs_list(skip: int = 0, limit: int = 10):
  """Get a list of Batch jobs endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        LmsJobsListResponseModel: list of Batch jobs objects.
        InternalServerErrorResponseModel:
            if the get batch jobs list raises an exception.
    """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")

    lms_job_data = LmsJob.fetch_all(skip=skip, limit=limit)
    lms_job_list = list(lms_job_data)

    return {"data": lms_job_list}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    print(e.message)
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{lms_job_id}", response_model=LmsJobResponseModel)
def get_lms_job(lms_job_id: str):
  """Get a Batch jobs using the batch job id endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        LmsJobResponseModel: details of the given Batch job.
        InternalServerErrorResponseModel:
            if the get batch jobs list raises an exception.
    """
  try:
    lms_job = LmsJob.find_by_id(lms_job_id)
    lms_job_data = lms_job.to_dict()

    return {"data": lms_job_data}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    print(e.message)
    Logger.error(e)
    raise InternalServerError(str(e)) from e

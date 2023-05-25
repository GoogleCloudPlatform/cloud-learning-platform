'''Batch Job Endpoint'''
from fastapi import APIRouter
from common.models import BatchJob
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import ResourceNotFound, InternalServerError, BadRequest
from schemas.batch_job import (BatchJobsListResponseModel,
                               BatchJobResponseModel)
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


@router.get("", response_model=BatchJobsListResponseModel)
def get_batch_jobs_list(skip: int = 0, limit: int = 10):
  """Get a list of Batch jobs endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        BatchJobsListResponseModel: list of Batch jobs objects.
        InternalServerErrorResponseModel:
            if the get batch jobs list raises an exception.
    """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")

    batch_job_data = BatchJob.fetch_all(skip=skip, limit=limit)
    batch_job_list = list(batch_job_data)

    return {"data": batch_job_list}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    print(e.message)
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{batch_job_id}", response_model=BatchJobResponseModel)
def get_batch_job(batch_job_id: str):
  """Get a list of Batch jobs endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        BatchJobsListResponseModel: list of Batch jobs objects.
        InternalServerErrorResponseModel:
            if the get batch jobs list raises an exception.
    """
  try:
    batch_job = BatchJob.find_by_id(batch_job_id)
    batch_job_data = batch_job.to_dict()

    return {"data": batch_job_data}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    print(e.message)
    Logger.error(e)
    raise InternalServerError(str(e)) from e

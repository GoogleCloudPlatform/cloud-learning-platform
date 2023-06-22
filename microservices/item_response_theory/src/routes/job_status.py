"""Returns Job Status"""

import traceback
from fastapi import APIRouter
from services.job_status import (check_job_status, delete_batch_job,
                                 remove_job_and_update_status)
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)
# pylint: disable=broad-except

router = APIRouter(
    prefix="/jobs",
    tags=["Job Status"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.get(
    "/{job_name}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_job_status(job_name: str):
  """Return Job Status"""
  try:
    data = check_job_status(job_name)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully fetched job status",
      "data": data
  }


@router.get("/")
def get_all_job_status():
  """Return all Job Status"""
  try:
    data = check_job_status(False)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully fetched job status",
      "data": data
  }


@router.delete(
    "/{job_name}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_batch_job_route(job_name: str):
  """Return Job Status"""
  try:
    delete_batch_job(job_name)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {"success": True, "message": "Successfully deleted", "data": {}}


@router.put(
    "/{job_name}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_state_and_remove_job_route(job_name: str):
  """Return Job Status"""
  try:
    remove_job_and_update_status(job_name)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {"success": True, "message": "Successfully updated", "data": {}}

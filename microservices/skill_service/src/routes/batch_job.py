""" Batch job endpoints """
from fastapi import APIRouter
from typing_extensions import Literal
from services.batch_job import (get_all_jobs, get_job_status, delete_batch_job,
                                remove_job_and_update_status)
import traceback
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from schemas.error_schema import NotFoundErrorResponseModel
from config import ERROR_RESPONSES

# pylint: disable = broad-except,invalid-name

router = APIRouter(
    prefix="/jobs",
    tags=["Batch Jobs"],
    responses=ERROR_RESPONSES)

JOB_TYPES = Literal["emsi_ingestion", "csv_ingestion", "unified_alignment",
                    "credential_engine_ingestion", "skill_embedding_db_update",
                    "role_skill_alignment", "knowledge_embedding_db_update",
                    "osn_ingestion", "e2e_test", "generic_csv_ingestion"]


@router.get(
    "/{job_type}/{job_name}",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_batch_job_status(job_type: JOB_TYPES, job_name: str):
  try:
    if job_name:
      data = get_job_status(job_type, job_name)
      response = {
          "success": True,
          "message": "Successfully fetched the batch job",
          "data": data
      }
      return response
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get("/{job_type}")
def get_all_job_status(job_type: JOB_TYPES):
  try:
    data = get_all_jobs(job_type)
    response = {
        "success":
            True,
        "message":
            f"Successfully fetched all the batch jobs of type {job_type}",
        "data":
            data
    }
    return response
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/{job_type}/{job_name}",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_batch_job_status(job_type: JOB_TYPES, job_name: str):
  try:
    delete_batch_job(job_type, job_name)
    response = {
        "success": True,
        "message": "Successfully deleted the batch job",
        "data": {}
    }
    return response

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/{job_type}/{job_name}",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_batch_job_status(job_type: JOB_TYPES, job_name: str):
  try:
    return remove_job_and_update_status(job_type, job_name)
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

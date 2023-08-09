# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable = broad-except,unused-import

""" Service to monitor batch jobs """
import traceback
from fastapi import APIRouter
from common.utils.batch_jobs import (get_all_jobs, get_job_status,
                                     delete_batch_job,
                                     remove_job_and_update_status)
from common.utils.config import JobTypes
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from schemas.error_schema import NotFoundErrorResponseModel
from schemas.jobs_schema import (JobGetStatusResponse,
                                 AllJobsGetStatusResponse,
                                 JobDeleteResponse)
from config import ERROR_RESPONSES
# pylint: disable = broad-except


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
    responses=ERROR_RESPONSES)

@router.get(
    "/{job_type_const}/{job_name}",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }},
    response_model=JobGetStatusResponse)
def get_batch_job_status(job_type_const: JobTypes, job_name: str):
  """ Get status of job by type and name """
  job_type = job_type_const.value
  try:
    data = get_job_status(job_type, job_name)
    response = {
        "success": True,
        "message": "Successfully retrieved batch job",
        "data": data
    }
    return response
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get("/{job_type_const}", response_model=AllJobsGetStatusResponse)
def get_all_job_status(job_type_const: JobTypes):
  """ Get status of all jobs by type """
  job_type = job_type_const.value
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
    "/{job_type_const}/{job_name}",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }},
    response_model=JobDeleteResponse)
def delete_batch_job_model(job_type_const: JobTypes, job_name: str):
  """ Delete batch job model by type and name.  Note this does
      not delete the Kubernetes Job. """
  job_type = job_type_const.value
  try:
    delete_batch_job(job_type, job_name)
    response = {
        "success": True,
        "message": "Successfully deleted the batch job",
        "data": None
    }
    return response

  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/{job_type_const}/{job_name}",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }},
    response_model=JobDeleteResponse)
def remove_batch_job(job_type_const: JobTypes, job_name: str):
  """ Remove job and update status by type and name """
  job_type = job_type_const.value
  try:
    remove_job_and_update_status(job_type, job_name)
    response = {
        "success": True,
        "message": "Successfully removed the batch job",
        "data": None
    }
    return response
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e

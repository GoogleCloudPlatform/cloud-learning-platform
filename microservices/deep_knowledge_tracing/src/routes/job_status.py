"""Returns Job Status"""

import traceback
from fastapi import APIRouter
from services.batch_job import (get_exp_status, get_all_experiments,delete_experiment,
remove_experiment_and_update_status)
from config import DKT_JOB_TYPE
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)
# pylint: disable=broad-except

router = APIRouter(
    prefix="/experiments",
    tags=["Deep Knowledge Tracing"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })

@router.post("/{experiment_id}/inference",include_in_schema=False,
      responses={404: {
        "model": NotFoundErrorResponseModel
    }})
#pylint: disable=unused-argument
def experiment_inference_route(experiment_id: str,
  activity: dict):
  """Route to get predictions for an experiment"""
  try:
    #TODO impelement experiment level predictions
    pass
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
      "message": "Successfully generated predictons",
      "data": {}
  }

@router.get(
    "/{experiment_id}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def job_status(experiment_id: str):
  """Returns Exp Status"""
  try:
    data = get_exp_status(DKT_JOB_TYPE,experiment_id)
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
      "message": "Successfully fetched experiment details",
      "data": data
  }


@router.get("/")
def get_all_exp_status():
  """Return all Exp Status"""
  try:
    data = get_all_experiments(DKT_JOB_TYPE)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully fetched all experiments",
      "data": data
  }


@router.delete(
    "/{experiment_id}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_experiment_route(experiment_id: str):
  """Delete Exp Status"""
  try:
    delete_experiment(DKT_JOB_TYPE,experiment_id)
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
    "/{experiment_id}", responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_state_and_remove_job_route(experiment_id: str):
  """Abort Experiment"""
  try:
    remove_experiment_and_update_status(DKT_JOB_TYPE,experiment_id)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {"success": True, "message": "Successfully updated", "data": {}}

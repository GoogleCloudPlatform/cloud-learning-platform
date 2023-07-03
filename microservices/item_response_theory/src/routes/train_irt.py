"""Train IRT Model"""

import traceback
from typing import Optional
from schemas.train_irt_schema import TrainIRTRequest
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel,
                                  NotFoundErrorResponseModel)
from services.update_assessment_items import update_assessment_items
from services.update_user_abilities import update_user_abilites
from services.get_all_learning_units import get_all_learning_units
from services.train import train_type_one, train_type_two
from fastapi import APIRouter
import json
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import InternalServerError, ResourceNotFound
from common.utils.kf_job_app import (kube_create_job,
                                     kube_get_namespaced_deployment_image_path)
from common.utils.logging_handler import Logger
from config import (JOB_NAMESPACE, GCP_PROJECT, CONTAINER_NAME, DEPLOYMENT_NAME,
                    BATCH_JOB_LIMITS, BATCH_JOB_REQUESTS)

router = APIRouter(
    prefix="/train",
    tags=["Train IRT Model"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })
# pylint: disable=dangerous-default-value


@router.post("/level")
def train_irt_on_level(request_body: TrainIRTRequest):
  """Starts IRT training at a particular level"""
  try:
    Logger.info("Request Body for batch Job: {}".format(request_body))
    image_path = kube_get_namespaced_deployment_image_path(
        DEPLOYMENT_NAME, CONTAINER_NAME, JOB_NAMESPACE, GCP_PROJECT)
    job_specs = {
        "container_image": image_path,
        "type": "item-response-theory",
        "input_data": json.dumps({**request_body.dict()}),
        "limits": BATCH_JOB_LIMITS,
        "requests": BATCH_JOB_REQUESTS
    }
    env_vars = {"GCP_PROJECT": GCP_PROJECT}
    data = kube_create_job(job_specs, JOB_NAMESPACE, env_vars)
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return {
      "success": True,
      "message": "Successfully started IRT training",
      "data": data
  }


def start_training_in_batch_job(request_body):
  all_learning_units = get_all_learning_units(
      level=request_body["level"], doc_id=request_body["id"])
  for index, lu in enumerate(all_learning_units):
    print("Count: ", index)
    train_irt(lu, request_body["update_collections"], "2pl", "2")
  return {"success": True, "message": "Successfully trained the IRT Model"}


@router.post("/", responses={404: {"model": NotFoundErrorResponseModel}})
def train_irt(learning_unit: str,
              update_collections: Optional[bool] = False,
              model_type: Optional[str] = "2pl",
              method: Optional[str] = "2"):
  """Starts IRT training at a learning unit level"""
  try:
    if method == "1":
      result = train_type_one(learning_unit, model_type)
    else:
      result = train_type_two(learning_unit, model_type)

    if update_collections:
      update_user_abilites(result["user_ability"], learning_unit)
      update_assessment_items(result["item_difficulty"],
                              result["item_discrimination"],
                              result["item_type_dict"], model_type)
  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
  return result

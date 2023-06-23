"""controller for course level"""
# pylint: disable=redefined-builtin,broad-exception-raised

import os
import json

from services.lu_inference import LearningUnitService
from services.validations import check_valid_request
from common.utils.kf_job_app import (kube_create_job,
                                     kube_get_namespaced_deployment_image_path)
from common.utils.logging_handler import Logger
from config import (JOB_NAMESPACE, GCP_PROJECT, CONTAINER_NAME,
                    DEPLOYMENT_NAME, BATCH_JOB_LIMITS, BATCH_JOB_REQUESTS)


class LearningUnitController():
  """controller class for learning unit level"""
  learning_unit = LearningUnitService()

  @staticmethod
  def create_lu_controller_method(parent_id, request_body):
    """controller method to create a learning unit"""
    if parent_id:
      return LearningUnitController.learning_unit.create_learning_unit(
        parent_id, request_body)
    else:
      raise Exception("learning objective id is missing in the URL")

  @staticmethod
  async def update_lu_controller_method(id, request_body):
    """controller method to update a learning unit"""
    if id:
      return await LearningUnitController.learning_unit.update_learning_unit(
        id, request_body)
    else:
      raise Exception("learning unit ID is missing in the URL")

  @staticmethod
  def get_lu_controller_method(id):
    """controller method to get a learning unit by id"""
    if id:
      return LearningUnitController.learning_unit.get_learning_unit(id)
    else:
      raise Exception("learning unit ID is missing in the URL")

  @staticmethod
  def get_all_lu_controller_method(parent_id):
    """controller method to get all learning units"""
    if parent_id:
      return LearningUnitController.learning_unit.get_all_learning_units(
        parent_id)
    else:
      raise Exception("learning objective ID is missing in the URL")

  @staticmethod
  def delete_lu_controller_method(id):
    """controller method to delete a learning unit"""
    if id:
      return LearningUnitController.learning_unit.delete_learning_unit(id)
    else:
      raise Exception("learning unit ID is missing in the URL")

  @staticmethod
  def create_lu_from_lo_controller_method(lo_id, request_body):
    Logger.info("Request Body for batch Job: {}".format(request_body))
    check_valid_request({"id": lo_id})
    if lo_id:
      request_body["lo_id"] = lo_id
      request_body["title"] = "Learning_Unit_Generation_{}".format(lo_id)
      image_path = kube_get_namespaced_deployment_image_path(DEPLOYMENT_NAME,
                                                             CONTAINER_NAME,
                                                             JOB_NAMESPACE,
                                                             GCP_PROJECT)
      job_specs = {
        "container_image": image_path,
        "type": "course-ingestion_learning-units",
        "input_data": json.dumps(request_body),
        "limits": BATCH_JOB_LIMITS,
        "requests": BATCH_JOB_REQUESTS
      }
      env_vars = {"GCP_PROJECT": GCP_PROJECT,
                  "DATABASE_PREFIX": os.getenv("DATABASE_PREFIX", "")}
      return kube_create_job(job_specs, JOB_NAMESPACE, env_vars)
    else:
      raise Exception("Learning Objective ID is missing in the URL")

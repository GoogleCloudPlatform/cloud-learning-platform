"""controller for learning content level"""
import json
import os
from services import learning_content_inference
from services.validations import check_file_exists
from common.utils.kf_job_app import (kube_create_job,
                                     kube_get_namespaced_deployment_image_path)
from common.utils.logging_handler import Logger
from common.models import LearningContentItem
from config import (JOB_NAMESPACE, GCP_PROJECT, CONTAINER_NAME,
                    DEPLOYMENT_NAME, BATCH_JOB_LIMITS, BATCH_JOB_REQUESTS)
from utils.exception_handlers import LearningContentIDMissing
# pylint: disable=redefined-builtin,broad-exception-raised

class LearningContentController:
  """controller class for course level"""

  @staticmethod
  def create_learning_content_controller_method(request_body):
    """controller method to create a Learning Content"""
    Logger.info("Request Body for batch Job: {}".format(request_body))
    data = request_body

    lc_title =  LearningContentItem.collection.filter( \
      "title","==",data["title"]).get()
    if lc_title:
      raise Exception("LC for the given title exists, "\
         "Please try with a different title")

    if isinstance(data, dict) and "start_page" in data and "end_page" in data:
      start_page = data["start_page"]
      end_page = data["end_page"]

      if start_page < 0 or end_page < 0:
        raise Exception("The Start Page value or End page value should "
                        "not be negative value")
      elif start_page > end_page:
        raise Exception("End page cannot be less than start page")
    if not check_file_exists(request_body.get("gcs_path")):
      raise Exception("Invalid GCS Path")

    image_path = kube_get_namespaced_deployment_image_path(DEPLOYMENT_NAME,
                                                           CONTAINER_NAME,
                                                           JOB_NAMESPACE,
                                                           GCP_PROJECT)
    job_specs = {
      "container_image": image_path,
      "type": "course-ingestion",
      "input_data": json.dumps(request_body),
      "limits": BATCH_JOB_LIMITS,
      "requests": BATCH_JOB_REQUESTS
    }
    env_vars = {"GCP_PROJECT": GCP_PROJECT,
                "DATABASE_PREFIX": os.getenv("DATABASE_PREFIX", "")}
    return kube_create_job(job_specs, JOB_NAMESPACE, env_vars)

  @staticmethod
  def update_learning_content_controller_method(id, request_body):
    """controller method to update a Learning Content"""
    if id:
      override = request_body.pop("override_existing_competencies", False)
      if override:
        return learning_content_inference.update_learning_content(
          id, request_body)
      else:
        return learning_content_inference.add_competencies(id, request_body)
    else:
      raise Exception("Learning Content ID is missing in the URL")

  @staticmethod
  def get_learning_content_controller_method(id):
    """controller method to get a Learning Content"""
    if id:
      return learning_content_inference.get_learning_content(id)
    else:
      raise Exception("Learning Content ID is missing in the URL")

  @staticmethod
  def get_all_learning_content_items_controller_method():
    """controller method to get all Learning Content Items"""
    return learning_content_inference.get_all_learning_contents()

  @staticmethod
  def delete_learning_content_controller_method(content_id: str) -> None:
    """
    A controller method to delete an LC and remove competency from that LC
    Parameters
    ----------
    content_id: str
    Return
    ------
    None
    """
    if content_id:
      return learning_content_inference. \
        delete_learning_content(content_id=content_id)
    else:
      raise LearningContentIDMissing("Learning Content ID is "
                                     "missing in the URL")

  @staticmethod
  def get_all_contents(skip: int, limit: int, sort_by: str,
                       order_by: str, search_query: str) -> dict:
    """
    Function for get all contents
    :param skip: int
    :param limit: int
    :param sort_by: str
    :param order_by: str
    :param search_query: str
    :return: dict
    """

    return learning_content_inference. \
      get_learning_contents(skip=skip, limit=limit, sort_by=sort_by,
                            order_by=order_by, search_query=search_query)

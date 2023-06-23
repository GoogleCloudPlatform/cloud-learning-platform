"""controller for node level topic tree"""
import os
import json

from services import topic_tree_inference
from services.validations import check_valid_request
from common.utils.kf_job_app import (kube_create_job,
                                     kube_get_namespaced_deployment_image_path)
from common.utils.logging_handler import Logger
from config import (JOB_NAMESPACE, GCP_PROJECT,
                    CONTAINER_NAME, DEPLOYMENT_NAME,
                    BATCH_JOB_LIMITS, BATCH_JOB_REQUESTS)


class TopicTreeController():
  """controller class for course level"""

  @staticmethod
  def topic_tree_controller_method(request_body):
    Logger.info("Request Body for batch Job: {}".format(request_body))
    check_valid_request(request_body)
    image_path = kube_get_namespaced_deployment_image_path(DEPLOYMENT_NAME,
                                                           CONTAINER_NAME,
                                                           JOB_NAMESPACE,
                                                           GCP_PROJECT)
    request_body["title"] = "level_{}-id_{}".format(request_body["level"],
                                                    request_body["id"])
    job_specs = {
      "container_image": image_path,
      "type": "course-ingestion_topic-tree",
      "input_data": json.dumps(request_body),
      "limits": BATCH_JOB_LIMITS,
      "requests": BATCH_JOB_REQUESTS
    }
    env_vars = {"GCP_PROJECT": GCP_PROJECT,
                "DATABASE_PREFIX": os.getenv("DATABASE_PREFIX", "")}
    return kube_create_job(job_specs, JOB_NAMESPACE, env_vars)

  @staticmethod
  async def topic_tree_controller_update_method(request_body):
    return await topic_tree_inference.write_topic_tree(request_body)

  @staticmethod
  async def get_complete_tree(request_body):
    return await topic_tree_inference.get_complete_tree_async(request_body)

"""Entry point for batch job. Creates a learning content item"""

from services.learning_content_inference import create_learning_content
from services.topic_tree_inference import create_hierarchy
from services.lu_inference import LearningUnitService
from services.firebase_messaging import send_to_token
from common.models.batch_job import BatchJobModel
from common.utils.kf_job_app import kube_delete_job
from common.utils.errors import ResourceNotFoundException
from common.utils.logging_handler import Logger
import asyncio
import json
from absl import flags, app
from config import JOB_NAMESPACE

FLAGS = flags.FLAGS
flags.DEFINE_string("container_name", "",
                    "Name of the container in which job is running")
flags.mark_flag_as_required("container_name")


def main(argv):
  request_body = {}
  job = None
  try:
    del argv  # Unused.
    job = BatchJobModel.find_by_uuid(FLAGS.container_name)
    job.status = "active"
    job.update()
    request_body = json.loads(job.input_data)
    request_type = job.type
    Logger.debug(request_type)
    if request_type == "course-ingestion_topic-tree":
      asyncio.run(create_hierarchy(request_body))
    elif request_type == "course-ingestion_learning-units":
      learning_unit_service = LearningUnitService()
      asyncio.run(
        learning_unit_service.create_lu_from_lo(
          request_body["lo_id"], request_body))
    else:
      learning_content_item = asyncio.run(create_learning_content(request_body))
      job.generated_item_id = learning_content_item["id"]
    job.status = "succeeded"
    job.update()
    if JOB_NAMESPACE == "default":
      kube_delete_job(FLAGS.container_name, JOB_NAMESPACE)
  except ResourceNotFoundException as e:
    Logger.info("Job failed. Error: %s" % str(e))
    Logger.info("Batch job with id %s not found" % FLAGS.container_name)
    request_body = {}
    raise e
  except Exception as e:
    Logger.error("Job failed. Error: %s" % str(e))
    job = BatchJobModel.find_by_uuid(FLAGS.container_name)
    job.status = "failed"
    job.errors = {
      "error_message": str(e)
    }
    job.update()
    Logger.error("Namespace: %s" % JOB_NAMESPACE)
    request_body = {}
    raise e
  finally:
    fcm_token = request_body.get("fcm_token", None)
    if fcm_token:
      response_body = {}
      response_body["job_name"] = job.name
      response_body["status"] = job.status
      if job.generated_item_id:
        response_body["generated_item_id"] = job.generated_item_id
      if job.output_gcs_path:
        response_body["output_gcs_path"] = job.output_gcs_path
      send_to_token(fcm_token, "Content Ingestion Job Status",
                    str(json.dumps(response_body)))


if __name__ == "__main__":
  app.run(main)

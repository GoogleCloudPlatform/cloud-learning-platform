"""Entry point for batch job"""
import json
from absl import flags, app
from common.utils.logging_handler import Logger
from common.utils.kf_job_app import kube_delete_job
from common.models.batch_job import BatchJobModel

from services.zip_file_processor import recreate_zip_structure_on_gcs

from config import (JOB_NAMESPACE, VALIDATE_AND_UPLOAD_ZIP)
# pylint: disable = broad-exception-raised

FLAGS = flags.FLAGS
flags.DEFINE_string("container_name", "",
                    "Name of the container in which job is running")
flags.mark_flag_as_required("container_name")


def main(argv):
  """Entry point method for batch job"""
  try:
    del argv  # Unused.
    job = BatchJobModel.find_by_uuid(FLAGS.container_name)
    job.status = "active"
    job.update()
    request_body = json.loads(job.input_data)
    if job.type == VALIDATE_AND_UPLOAD_ZIP:
      _ = recreate_zip_structure_on_gcs(request_body)
    else:
      raise Exception("Invalid job type")
    job.status = "succeeded"
    job.update()
    if JOB_NAMESPACE == "default":
      kube_delete_job(FLAGS.container_name, JOB_NAMESPACE)
  except Exception as e:
    Logger.info(f"Job failed. Error: {str(e)}")
    job = BatchJobModel.find_by_uuid(FLAGS.container_name)
    job.status = "failed"
    job.errors = {"error_message": str(e)}
    job.update()
    Logger.info(f"Namespace: {JOB_NAMESPACE}")

    raise e


if __name__ == "__main__":
  Logger.info("run_batch_job file for content-serving was triggered")
  app.run(main)

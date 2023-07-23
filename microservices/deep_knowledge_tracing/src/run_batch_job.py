"""Entry point for batch job. Runs DKT Model"""

from services.train import Trainer
from common.models import BatchJobModel
from common.utils.kf_job_app import kube_delete_job
from common.utils.logging_handler import Logger
import json
from config import JOB_NAMESPACE
from absl import flags, app

FLAGS = flags.FLAGS
flags.DEFINE_string("container_name", "",
                    "Name of the container in which job is running")
flags.mark_flag_as_required("container_name")



def main(argv):
  try:
    del argv  # Unused.
    job = BatchJobModel.find_by_uuid(FLAGS.container_name)
    request_body = json.loads(job.input_data)
    history,evaluation_scores = Trainer.train(request_body)
    job.status = "succeeded"
    metadata = {"history": history,
                "evaluation_scores" : evaluation_scores}
    job.metadata = metadata
    job.update()
    if JOB_NAMESPACE == "default":
      kube_delete_job(FLAGS.container_name, JOB_NAMESPACE)
  except Exception as e:
    Logger.info("Job failed. Error: %s" % str(e))
    job = BatchJobModel.find_by_uuid(FLAGS.container_name)
    job.status = "failed"
    job.update()
    Logger.info("Namespace: %s" % JOB_NAMESPACE)
    raise e


if __name__ == "__main__":
  app.run(main)

"""Entry point for batch job"""
import json
from absl import flags, app
from common.utils.logging_handler import Logger
from common.utils.kf_job_app import kube_delete_job
from common.models.batch_job import BatchJobModel
from services.skill_to_knowledge.skill_to_passage import (
    batch_populate_knowledge_embeddings)
from services.search.search import (batch_populate_skill_embeddings,
                                    batch_populate_kg_embeddings)
from services.ingest_credential_engine import ingest_credential_engine
from services.ingest_csv import ingest_csv
from services.ingest_emsi import ingest_emsi
from services.ingest_osn import ingest_osn_csv
from services.ingest_generic_csv import ingest_generic_csv
from services.skill_parsing.skill_parsing import batch_update_role_to_skills
from services.skill_unified_alignment.skill_unified_alignment import (
    batch_unified_alignment)
from config import (JOB_NAMESPACE, ROLE_SKILL_MAPPING_JOB_TYPE,
                    CE_INGESTION_JOB_TYPE, GENERIC_CSV_INGESTION_JOB_TYPE,
                    CSV_INGESTION_JOB_TYPE, EMSI_INGESTION_JOB_TYPE,
                    OSN_INGESTION_JOB_TYPE, UNIFIED_ALIGNMENT_JOB_TYPE,
                    POPULATE_SKILL_EMBEDDING_JOB_TYPE,
                    POPULATE_KNOWLEDGE_EMBEDDING_JOB_TYPE,
                    CREATE_KG_EMBEDDING_JOB_TYPE)

# pylint: disable=broad-exception-raised

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
    if job.type == UNIFIED_ALIGNMENT_JOB_TYPE:
      _ = batch_unified_alignment(request_body)
    elif job.type == CE_INGESTION_JOB_TYPE:
      _ = ingest_credential_engine(request_body.get("links"))
    elif job.type == CSV_INGESTION_JOB_TYPE:
      _ = ingest_csv(request_body)
    elif job.type == EMSI_INGESTION_JOB_TYPE:
      _ = ingest_emsi(request_body.get("size"))
    elif job.type == OSN_INGESTION_JOB_TYPE:
      _ = ingest_osn_csv(request_body)
    elif job.type == GENERIC_CSV_INGESTION_JOB_TYPE:
      _ = ingest_generic_csv(request_body)
    elif job.type == POPULATE_SKILL_EMBEDDING_JOB_TYPE:
      _ = batch_populate_skill_embeddings(request_body)
    elif job.type == POPULATE_KNOWLEDGE_EMBEDDING_JOB_TYPE:
      _ = batch_populate_knowledge_embeddings(request_body)
    elif job.type == CREATE_KG_EMBEDDING_JOB_TYPE:
      _ = batch_populate_kg_embeddings(request_body)
    elif job.type == ROLE_SKILL_MAPPING_JOB_TYPE:
      _ = batch_update_role_to_skills(request_body)
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
  Logger.info("run_batch_job file for skill-service was triggered")
  app.run(main)

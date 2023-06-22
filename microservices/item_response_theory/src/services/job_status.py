"""Function to check Job Status"""

from common.models import BatchJobModel
from common.utils.kf_job_app import kube_delete_job
from common.utils.logging_handler import Logger
from config import JOB_NAMESPACE
import json

# pylint: disable=broad-except,broad-exception-raised
def check_job_status(job_name):
  """returns status of the batch job"""
  if job_name:
    job = BatchJobModel.find_by_name(job_name)
    job_response = {}
    job_response["job_name"] = job.name
    job_response["created_by"] = job.created_by
    job_response["created_time"] = str(job.created_time)
    job_response["last_modified_by"] = job.last_modified_by
    job_response["last_modified_time"] = str(job.last_modified_time)
    job_response["input_data"] = json.loads(job.input_data)
    job_response["status"] = job.status
    return job_response
  else:
    jobs = list(BatchJobModel.collection.filter(
      type="item-response-theory").fetch())
    job_list = []
    jobs.sort(key = lambda x:x.created_time,reverse=True)
    for job in jobs:
      job_response = {}
      job_response["job_name"] = job.name
      job_response["created_by"] = job.created_by
      job_response["created_time"] = str(job.created_time)
      job_response["last_modified_by"] = job.last_modified_by
      job_response["last_modified_time"] = str(job.last_modified_time)
      job_response["input_data"] = json.loads(job.input_data)
      job_response["status"] = job.status
      job_list.append(job_response)
    response = {}
    for i in job_list:
      response[str(job_list.index(i))] = i
    return response

def delete_batch_job(job_name):
  """Deletes a particular batch job"""
  job = BatchJobModel.find_by_name(job_name)
  try:
    job.delete_by_id(job.id)
  except Exception as e:
    raise Exception("Internal server error") from e

def remove_job_and_update_status(job_name):
  """Removes a particular batch job from namespace
  and updates the status in firestore"""
  try:
    kube_delete_job(job_name, JOB_NAMESPACE)
  except Exception as e:
    Logger.info("Failed to remove job from namespace: " + str(e))
    pass
  job = BatchJobModel.find_by_name(job_name)
  try:
    if job.status == "active":
      job.status = "aborted"
      job.update()
  except Exception as e:
    raise Exception("Failed to update status") from e

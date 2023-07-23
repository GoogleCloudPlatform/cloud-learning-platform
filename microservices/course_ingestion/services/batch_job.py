"""Module for job related functions"""

import json
from common.models.batch_job import BatchJobModel
from common.utils.kf_job_app import kube_delete_job
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from config import JOB_NAMESPACE

# pylint: disable=broad-except,broad-exception-raised
def get_job_status(job_name):
  """returns status of the batch job"""
  if job_name:
    try:
      job = BatchJobModel.find_by_uuid(job_name)
    except ResourceNotFoundException:
      job = BatchJobModel.find_by_name(job_name)
    job_response = {}
    job_response["job_name"] = job.name
    job_response["created_by"] = job.created_by
    job_response["created_time"] = str(job.created_time)
    job_response["last_modified_by"] = job.last_modified_by
    job_response["last_modified_time"] = str(job.last_modified_time)
    if job.input_data:
      job_response["input_data"] = json.loads(job.input_data)
    else:
      job_response["input_data"] = None
    job_response["status"] = job.status
    job_response["type"] = job.type
    job_response["errors"] = job.errors
    if job.status == "succeeded":
      job_response["generated_item_id"] = job.generated_item_id
    return job_response
  else:
    jobs = list(BatchJobModel.collection.filter(
      "type", "in", ["course-ingestion",
      "course-ingestion_learning-units","course-ingestion_topic-tree"]
      ).fetch())
    job_list = []
    jobs.sort(key = lambda x:x.created_time,reverse=True)
    for job in jobs:
      job_response = {}
      job_response["job_name"] = job.name
      job_response["created_by"] = job.created_by
      job_response["created_time"] = str(job.created_time)
      job_response["last_modified_by"] = job.last_modified_by
      job_response["last_modified_time"] = str(job.last_modified_time)
      if job.input_data:
        job_response["input_data"] = json.loads(job.input_data)
      else:
        job_response["input_data"] = None
      job_response["status"] = job.status
      job_response["type"] = job.type
      job_response["errors"] = job.errors
      if job.status == "succeeded" and job.type=="course-ingestion":
        job_response["generated_item_id"] = job.generated_item_id
      job_list.append(job_response)
    response = {}
    for i in job_list:
      response[str(job_list.index(i))] = i
    return response


def delete_batch_job(job_name):
  """Deletes a particular batch job"""
  try:
    job = BatchJobModel.find_by_uuid(job_name)
  except ResourceNotFoundException:
    job = BatchJobModel.find_by_name(job_name)
  try:
    job.delete_by_id(job.uuid)
  except Exception as e:
    raise Exception("Internal server error") from e

def remove_job_and_update_status(job_name):
  """Removes a particular batch job from namespace
  and updates the status in firestore"""
  try:
    job = BatchJobModel.find_by_uuid(job_name)
  except ResourceNotFoundException:
    job = BatchJobModel.find_by_name(job_name)
  try:
    kube_delete_job(job.uuid, JOB_NAMESPACE)
  except Exception as e:
    Logger.info("Failed to remove job from namespace: " + str(e))
    pass
  try:
    if job.status == "active":
      job.status = "aborted"
      job.update()
  except Exception as e:
    raise Exception("Failed to update status") from e

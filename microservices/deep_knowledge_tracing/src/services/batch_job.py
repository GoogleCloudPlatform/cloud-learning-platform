"""Module for job related functions"""

from common.models.batch_job import BatchJobModel
from common.utils.kf_job_app import (kube_delete_job, kube_create_job,
                                     kube_get_namespaced_deployment_image_path)
import json
from common.utils.errors import ResourceNotFoundException, ConflictError
from config import (DEPLOYMENT_NAME, CONTAINER_NAME, JOB_NAMESPACE, GCP_PROJECT,
                    BATCH_JOB_LIMITS, BATCH_JOB_REQUESTS)
# pylint: disable = dangerous-default-value,broad-exception-raised


def initiate_batch_job(request_body, job_type, env_vars={}):
  """Triggers a batch job to map skills to knowledge nodes
    Args:
      req_body: dict - dictionary containing metadata for running batch job
      job_type: "type of job"
      env_vars: environment variables
    Returns:
      job_status: status message if the batch job is triggered successfully
                  or not.
  """
  image_path = kube_get_namespaced_deployment_image_path(
      DEPLOYMENT_NAME, CONTAINER_NAME, JOB_NAMESPACE, GCP_PROJECT)
  job_specs = {
      "container_image": image_path,
      "type": job_type,
      "input_data": json.dumps(request_body),
      "limits": BATCH_JOB_LIMITS,
      "requests": BATCH_JOB_REQUESTS
  }
  env_vars.update({"GCP_PROJECT": GCP_PROJECT})
  job_status = kube_create_job(job_specs, JOB_NAMESPACE, env_vars)
  response = {}
  if job_status.get("status"):
    response = {
        "success": True,
        "message": f"Successfully initiated the experiment with type \
        '{job_type}'. "\
              "Please use the experiment id to track status",
        "data": {
          "experiment_id": job_status.get("job_name"),
          "status": job_status.get("status")
        }
    }
  else:  # will go in else if any duplicate job found
    raise ConflictError("Job already running for same request")
  return response


def get_exp_status(job_type, experiment_id):
  """returns status of the batch job"""
  if experiment_id:
    job = BatchJobModel.collection.filter("type", "in", [job_type]).filter(
        "uuid", "==", experiment_id).get()
    if job:
      job_response = {}
      job_response["experiment_id"] = job.uuid
      job_response["created_by"] = job.created_by
      job_response["created_time"] = str(job.created_time)
      job_response["last_modified_by"] = job.last_modified_by
      job_response["last_modified_time"] = str(job.last_modified_time)
      job_response["input_data"] = json.loads(job.input_data)
      job_response["status"] = job.status
      job_response["errors"] = job.errors
      job_response["type"] = job.type
      if job.output_gcs_path:
        job_response["output_gcs_path"] = job.output_gcs_path
      if job.status == "succeeded":
        job_response["metadata"] = job.metadata
      return job_response
    else:
      raise ResourceNotFoundException("Experiment with this id does not exist")


def get_all_experiments(job_type):
  """
  Method to get all jobs of given type

  Args:
    job_type: type of job (e.g.: skill_alignment)
  Returns:
    response: containing success message
  """
  jobs = BatchJobModel.collection.filter("type", "in", [job_type]).fetch()
  job_list = []
  for job in jobs:
    job_response = {}
    job_response["experiment_id"] = job.uuid
    job_response["created_by"] = job.created_by
    job_response["created_time"] = str(job.created_time)
    job_response["last_modified_by"] = job.last_modified_by
    job_response["last_modified_time"] = str(job.last_modified_time)
    job_response["input_data"] = json.loads(job.input_data)
    job_response["status"] = job.status
    job_response["type"] = job.type
    job_response["errors"] = job.errors
    if job.output_gcs_path:
      job_response["output_gcs_path"] = job.output_gcs_path
    if job.status == "succeeded":
      job_response["metadata"] = job.metadata
    job_list.append(job_response)
  data_response = {}
  for i in job_list:
    data_response[str(job_list.index(i))] = i
  return data_response


def delete_experiment(job_type, experiment_id):
  """Deletes a particular batch job

  Args:
    job_type: type of job (e.g.: skill_alignment)
    job_name: name of the job
  Returns:
    response: containing success message
  """
  job = BatchJobModel.find_by_uuid(experiment_id)
  if job and job.type == job_type:
    try:
      job.delete_by_id(job.name)
    except Exception as e:
      raise Exception("Internal server error") from e
  else:
    raise ResourceNotFoundException(
        "Experiment with given id does not exist")


def remove_experiment_and_update_status(job_type, experiment_id):
  """Removes a particular batch job from namespace
  and updates the status in firestore

  Args:
    job_type: type of job (e.g.: skill_alignment)
    experiment_id: name of the job
  Returns:
    response: containing success message
  """
  job = BatchJobModel.find_by_uuid(experiment_id)
  if job and job.type == job_type:
    try:
      kube_delete_job(experiment_id, JOB_NAMESPACE)
    except Exception as e:
      raise Exception(
        "Failed to remove experiment from namespace: " + str(e)) from e
    try:
      if job.status == "active":
        job.status = "aborted"
        job.update()
        response = {
            "success":
                True,
            "message":
                "Successfully updated the status and " +
                "removed the experiment from namespace"
        }
        return response
    except Exception as e:
      raise Exception("Failed to update status") from e
  else:
    raise ResourceNotFoundException(
        "Job with given name and type does not exist")

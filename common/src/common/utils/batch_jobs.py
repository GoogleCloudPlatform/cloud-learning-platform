# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for job related functions"""

from common.models.batch_job import BatchJobModel, JobStatus
from common.utils.kf_job_app import (kube_delete_job, kube_create_job,
                                     kube_get_namespaced_deployment_image_path)
import json
from common.utils.errors import ResourceNotFoundException, ConflictError

from config import (DEPLOYMENT_NAME, CONTAINER_NAME, JOB_NAMESPACE, GCP_PROJECT)
# pylint: disable = dangerous-default-value,broad-exception-raised


def initiate_batch_job(request_body, job_type, env_vars={}):
  """Triggers a batch job
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
      "input_data": json.dumps(request_body)
  }
  env_vars.update({"GCP_PROJECT": GCP_PROJECT})
  job_status = kube_create_job(job_specs, JOB_NAMESPACE, env_vars)
  response = {}
  if job_status.get("status"):
    response = {
        "success": True,
        "message": f"Successfully initiated the job with type '{job_type}'. "\
              "Please use the job name to track the job status",
        "data": {
          "job_name": job_status.get("job_name"),
          "status": job_status.get("status")
        }
    }
  else:  # will go in else if any duplicate job found
    raise ConflictError("Job already running for same request")
  return response


def get_job_status(job_type, job_name):
  """returns status of the batch job"""
  job = BatchJobModel.collection.filter("type", "in", [job_type]).filter(
      "uuid", "==", job_name).get()
  if job:
    job_response = job.get_fields(reformat_datetime=True)
    return job_response
  else:
    raise ResourceNotFoundException(
        f"Job with name {job_name} and type {job_type} not found")


def get_all_jobs(job_type):
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
    job_response = job.get_fields(reformat_datetime=True)
    job_list.append(job_response)
  return job_list


def delete_batch_job(job_type, job_name):
  """Deletes a particular batch job model

  Args:
    job_type: type of job (e.g.: skill_alignment)
    job_name: name of the job
  Returns:
    response: containing success message
  """
  job = BatchJobModel.find_by_uuid(job_name)
  if job and job.type == job_type:
    try:
      job.delete_by_id(job.uuid)
    except Exception as e:
      raise Exception("Internal server error") from e
  else:
    raise ResourceNotFoundException(
        f"Job with name {job_name} and type {job_type} not found")


def remove_job_and_update_status(job_type, job_name):
  """Removes a particular batch job from namespace
  and updates the status in firestore

  Args:
    job_type: type of job (e.g.: skill_alignment)
    job_name: name of the job
  Returns:
    response: containing success message
  """
  job = BatchJobModel.find_by_uuid(job_name)
  if job and job.type == job_type:
    try:
      kube_delete_job(job_name, JOB_NAMESPACE)
    except Exception as e:
      raise Exception("Failed to remove job from namespace: " + str(e)) from e
    try:
      if job.status == JobStatus.JOB_STATUS_ACTIVE.value:
        job.status = JobStatus.JOB_STATUS_ABORTED.value
        job.update()
        response = {
            "success":
                True,
            "message":
                "Successfully updated the status and removed the job from " +
                "namespace"
        }
        return response
    except Exception as e:
      raise Exception("Failed to update status") from e
  else:
    raise ResourceNotFoundException(
        f"Job with name {job_name} and type {job_type} not found")

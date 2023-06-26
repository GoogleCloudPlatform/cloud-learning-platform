"""Utiliy functions for kubernetes job related operations"""

import os
import logging
import traceback
import uuid
import json
import sys
from datetime import datetime, timedelta
from pytz import timezone

from requests import JSONDecodeError
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from common.models.batch_job import BatchJobModel
from common.utils.config import (DEFAULT_JOB_LIMITS,
  DEFAULT_JOB_REQUESTS)
from common.utils.config import (JOB_TYPES_WITH_PREDETERMINED_TITLES,
                                 BATCH_JOB_FETCH_TIME,
                                 BATCH_JOB_PENDING_TIME_THRESHOLD,
                                 GCLOUD_LOG_URL)
#pylint: disable=dangerous-default-value
#pylint: disable=logging-not-lazy
#pylint: disable=consider-using-f-string
#pylint: disable=logging-format-interpolation
#pylint: disable=broad-exception-raised
#pylint: disable=invalid-name
# Set logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Setup K8 configs
config.load_incluster_config()
configuration = client.Configuration()
api_instance = client.BatchV1Api(client.ApiClient(configuration))

def kube_delete_empty_pods(namespace="default"):
  """
    This function deletes completed pods given a namespace
  """
  # The always needed object
  deleteoptions = client.V1DeleteOptions()
  # We need the api entry point for pods
  api_pods = client.CoreV1Api()
  # List the pods
  try:
    pods = api_pods.list_namespaced_pod(
        namespace, pretty=True, timeout_seconds=60)
    for pod in pods.items:
      logging.debug(pod)
      podname = pod.metadata.name
      try:
        if pod.status.phase == "Succeeded":
          api_pods.delete_namespaced_pod(podname, namespace, body=deleteoptions)
          logging.info("Pod: %s deleted!\n" % podname)
      except ApiException as e:
        logging.error(
            "Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)
  except TypeError as e:
    logging.error("Failed to delete pods: %s\n" % e)
  except ApiException as e:
    logging.error(
        "Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

def kube_delete_job(job_name, namespace="default"):
  """Deletes a pod with the given name"""
  # The always needed object
  deleteoptions = client.V1DeleteOptions(propagation_policy="Background")
  try:
    api_response = api_instance.delete_namespaced_job(
      job_name, namespace, body=deleteoptions)
    logging.info(api_response)
  except ApiException as e:
    raise Exception(
      "Exception when calling BatchV1Api->delete_namespaced_job: " + str(
        e)) from e
  except Exception as e:
    raise Exception("Failed to delete the job. Error: " + str(e)) from e

def kube_namespace_job_status(namespace="default"):
  """
    Function to get job status for every job present in the specified namespace.
    Status types - Succeeded, Failed, Active
  """
  try:
    jobs = api_instance.list_namespaced_job(
        namespace, pretty=True, timeout_seconds=60)

    jobs_status = []
    for job in jobs.items:
      jobname = job.metadata.name
      jobstatus = job.status.conditions
      if job.status.succeeded == 1:
        jobstatus = "succeeded"
      elif jobstatus is None and job.status.active == 1:
        jobstatus = "active"
      elif jobstatus and jobstatus[-1].type == "Failed" and \
          jobstatus[-1].status:
        jobstatus = "failed"
      else:
        jobstatus = "unknown"
      jobs_status.append({"name": jobname, "status": jobstatus})
    return jobs_status
  except TypeError as e:
    raise Exception("Internal server error") from e
  except ApiException as e:
    raise Exception(
        "Exception when calling BatchV1Api->list_namespaced_job") from e


def kube_cleanup_finished_jobs(namespace="default"):
  """
    This method checks for existing Finished Jobs and deletes them.
  """
  deleteoptions = client.V1DeleteOptions()
  try:
    jobs = api_instance.list_namespaced_job(
        namespace, pretty=True, timeout_seconds=60)
    for job in jobs.items:
      logging.debug(job)
      jobname = job.metadata.name
      jobstatus = job.status.conditions
      if job.status.succeeded == 1:
        # Clean up Job
        logging.info("Cleaning up Job: %s. Finished at: %s" % \
            (jobname, job.status.completion_time))
        try:
          # Setting Grace Period to 0 means delete ASAP.
          # Propagation policy makes the Garbage cleaning Async
          api_response = api_instance.delete_namespaced_job(
              jobname,
              namespace,
              body=deleteoptions,
              grace_period_seconds=0,
              propagation_policy="Background")
          logging.debug(api_response)
        except ApiException:
          print("Exception when calling BatchV1Api->delete_namespaced_job")
      else:
        if jobstatus is None and job.status.active == 1:
          jobstatus = "active"
        logging.info("Job: %s not cleaned up. Current status: %s" %
                     (jobname, jobstatus))

    # Cleaning the pods
    kube_delete_empty_pods(namespace)
    return
  except ApiException:
    logging.error("Exception when calling BatchV1Api->list_namespaced_job")


#pylint: disable=dangerous-default-value
def kube_create_job_object(name,
                           container_image,
                           limits,
                           requests,
                           namespace="default",
                           container_name="jobcontainer",
                           env_vars={}):
  """
    Create a k8 Job Object
    Minimum definition of a job object:
    {"api_version": None, - Str
    "kind": None,     - Str
    "metadata": None, - Metada Object
    "spec": None,     -V1JobSpec
    "status": None}   - V1Job Status
    V1Job -> V1ObjectMeta
          -> V1JobStatus
          -> V1JobSpec -> V1PodTemplate -> V1PodTemplateSpec -> V1Container
    """
  # Body is the object Body
  body = client.V1Job(api_version="batch/v1", kind="Job")
  # Body needs Metadata
  # Attention: Each JOB must have a different name!
  body.metadata = client.V1ObjectMeta(namespace=namespace, name=name)
  # And a Status
  body.status = client.V1JobStatus()
  # Template...
  template = client.V1PodTemplate()
  template.template = client.V1PodTemplateSpec()
  # Passing Arguments in Env:
  env_list = []
  for env_name, env_value in env_vars.items():
    env_list.append(client.V1EnvVar(name=env_name, value=env_value))
  resources = client.V1ResourceRequirements(
    limits=limits,
    requests=requests
  )
  container = client.V1Container(
      name=container_name,
      image=container_image,
      env=env_list,
      resources=resources,
      command=["python", "run_batch_job.py"],
      args=["--container_name", name])
  template.template.spec = client.V1PodSpec(
      containers=[container],
      restart_policy="Never",
      service_account_name="ksa")
  # And finaly we can create our V1JobSpec!
  body.spec = client.V1JobSpec(
      backoff_limit=0,
      template=template.template)
  return body


def kube_test_credentials():
  """
    Testing function.
    If you get an error on this call don"t proceed. Something is wrong on
    your connectivty to Google API.
    Check Credentials, permissions, keys, etc.
    Docs: https://cloud.google.com/docs/authentication/
  """
  try:
    api_response = api_instance.get_api_resources()
    logging.info(api_response)
  except ApiException as e:
    print("Exception when calling API: %s\n" % e)

def get_cloud_link(microservice_name):
  """Creates a query which can be used to directly view the logs of
  the required microservice"""
  # Fetching the required ENV variables to create the log query
  GCP_PROJECT = os.getenv("GCP_PROJECT")
  SKAFFOLD_NAMESPACE = os.getenv("SKAFFOLD_NAMESPACE")
  GKE_CLUSTER = os.getenv("GKE_CLUSTER")
  GCP_ZONE = os.getenv("GCP_ZONE")
  url = GCLOUD_LOG_URL
  # Fetching the current time in GMT
  tz = timezone("GMT")
  INIT_TIMESTAMP = datetime.now(tz)
  FINAL_TIMESTAMP = (INIT_TIMESTAMP + \
    timedelta(hours=-1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
  INIT_TIMESTAMP = INIT_TIMESTAMP.strftime("%Y-%m-%dT%H:%M:%S.000Z")
  # Replacing the values to get the correct URL
  url = url.replace("{GCP_PROJECT}", GCP_PROJECT)
  url = url.replace("{SKAFFOLD_NAMESPACE}", SKAFFOLD_NAMESPACE)
  url = url.replace("{GKE_CLUSTER}", GKE_CLUSTER)
  url = url.replace("{GCP_ZONE}", GCP_ZONE)
  url = url.replace("{INIT_TIMESTAMP}", INIT_TIMESTAMP)
  url = url.replace("{FINAL_TIMESTAMP}", FINAL_TIMESTAMP)
  url = url.replace("{MICROSERVICE}", microservice_name)

  return url

def kube_create_job(job_specs ,namespace="default", env_vars={}):
  """check for pending/active duplicate job"""
  job_logs = {}
  logging.info("Type of request body")
  logging.info(job_specs["input_data"])
  logging.info(type(job_specs["input_data"]))
  duplicate_job = find_duplicate_jobs(job_specs["type"],
                                      job_specs["input_data"])
  if duplicate_job:
    return duplicate_job

  # Create the job definition
  logging.info("Batch Job Creation Started")
  container_image = job_specs["container_image"]
  limits = job_specs.get("limits", DEFAULT_JOB_LIMITS)
  requests = job_specs.get("requests", DEFAULT_JOB_REQUESTS)
  name = str(uuid.uuid4())  #job name

  # creating a job entry in firestore
  job_model = BatchJobModel()
  job_model.id_ = name
  job_model.type = job_specs["type"]
  job_model.status = "pending"
  job_model.uuid = name
  job_model.save()
  logging.info("Batch Job {}: Started with job type " \
      "{}".format(job_model.name,job_model.type))
  logging.info("Batch Job {}: Updated Batch Job Status " \
      "to pending in firestore".format(job_model.name))
  if job_specs["type"] in JOB_TYPES_WITH_PREDETERMINED_TITLES:
    job_model.input_data = job_specs[
      "input_data"]  # data required for running job
    if isinstance(job_specs["input_data"], str):
      try:
        job_specs["input_data"] = json.loads(job_specs["input_data"])
      except JSONDecodeError as e:
        logging.info("Unable to convert job_specs['input_data'] to dict,\
          \nError: {}".format(e))
    if isinstance(job_specs["input_data"], dict) and \
      "title" in job_specs["input_data"].keys():
      job_model.name = job_specs["input_data"]["title"]
    else:
      job_model.name = name
  else:
    created_time = job_model.created_time
    job_name_suffix = str(created_time.year)+"-"+\
      str(created_time.month)+"-"+str(
      created_time.day)+"-"+str(created_time.hour)+"-"+\
      str(created_time.minute)+"-"+str(created_time.second)
    input_data = json.loads(job_specs["input_data"])
    input_data["title"] = input_data["title"] + "-" +\
      job_name_suffix
    job_specs["input_data"] = json.dumps(input_data)
    job_model.name = input_data["title"]
    job_model.input_data = job_specs[
        "input_data"]  # data required for running job

  if job_specs["type"] == "assessment-items":
    job_logs = {job_specs["type"]: get_cloud_link(job_specs["type"]),
                input_data["activity"]: get_cloud_link(
                  input_data["activity"].replace("_", "-"))}

  elif job_specs["type"] in ["course-ingestion",
                             "course-ingestion_topic-tree",
                             "course-ingestion_learning-units"]:
    job_logs = {job_specs["type"]: get_cloud_link("course-ingestion")}
  elif job_specs["type"] in ["deep-knowledge-tracing"]:
    job_logs = {job_specs["type"]: get_cloud_link("deep-knowledge-tracing")}
  else:
    job_logs = {}

  job_model.job_logs = job_logs

  job_model.update()

  body = kube_create_job_object(
    name=name,
    container_image=container_image,
    namespace=namespace,
    env_vars=env_vars,
    limits=limits,
    requests=requests)
  try:
    api_instance.create_namespaced_job(namespace, body, pretty=True)
    logging.info("Batch Job {}: Created".format(job_model.uuid))
    return {"job_name": job_model.uuid, "doc_id": job_model.id_,
    "status": "active", "job logs": job_logs}
  except ApiException as e:
    logging.error("Batch Job {}: Failed".format(job_model.uuid))
    logging.error(traceback.print_exc())
    BatchJobModel.delete_by_id(job_model.id)
    raise Exception(
        "Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e) \
            from e


def kube_get_namespaced_deployment_image_path(deployment_name,container_name,
                                                      namespace,gcp_project):
  """
    This function returns the image path for given deployment and container name
    args:
      deployment_name: (str)-name of the deployment to get
      container_name: (str)-name of the container to search
      namespace: (str)-namespace in which container is running
      gcp_project: (str)-GCP PROJECT ID
    returns:
      image_path: (str)- container image path
  """
  image_path = "gcr.io/{}/{}:latest".format(gcp_project,container_name)
  try:
    apis_api = client.AppsV1Api()
    resp = apis_api.read_namespaced_deployment(deployment_name,namespace)
    for container in resp.spec.template.spec.containers:
      if container_name==container.name:
        image_path = container.image.split("@")[0]
        break
  except ApiException as e:
    logging.info("---ERROR---")
    logging.info(e)
  return image_path


def find_duplicate_jobs(job_type, request_body=None):
  """input_data any duplicate batch jobs that are currently running in pending
  or active state for the given type and request_body

  Args:
    job_type: type of job (e.g.: course-ingestion_topic-tree)
    request_body: input_data passed to the batch job.
  Returns:
    message: containing success message
  """
  time = datetime.now() - timedelta(hours=BATCH_JOB_FETCH_TIME)
  data = BatchJobModel.collection.filter("created_time", ">", time).filter(
      "type", "==", job_type).filter("status", "in",
                                     ["pending", "active"]).fetch()
  if request_body:
    request_body = json.loads(request_body)
  for job in data:
    job = job.to_dict()
    name = job.get("name")
    status = job.get("status")
    input_data = {}
    if job.get("input_data"):
      input_data = json.loads(job.get("input_data"))

    created_time = datetime.fromtimestamp(job.get("created_time").timestamp())
    time_now_minus_10 = datetime.now() - timedelta(
        minutes=BATCH_JOB_PENDING_TIME_THRESHOLD)
    failed_msg = {
        "message":
            f"Job already running with name '{name}' and is in {status} state"
    }

    if status == "pending":
      if created_time >= time_now_minus_10:
        if (request_body and
            request_body == input_data) or request_body is None:
          return failed_msg
    elif status == "active":
      if (request_body and request_body == input_data) or request_body is None:
        return failed_msg

  # return empty if no duplicate jobs
  return {}

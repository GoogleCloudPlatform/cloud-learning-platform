"""config file """
import os
from common.utils.logging_handler import Logger

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT", "core-learning-services-dev")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT


SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write",
]

try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace","r",
  encoding="utf-8",errors="ignore") as ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

API_BASE_URL = os.getenv("API_BASE_URL")
SERVICE_NAME = os.getenv("SERVICE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() \
    in ("True", "true"))

SERVICES = {
}

BATCH_JOB_LIMITS = {
      "cpu": "3",
      "memory": "7000Mi"
    }
BATCH_JOB_REQUESTS = {
      "cpu": "3",
      "memory": "7000Mi"
    }

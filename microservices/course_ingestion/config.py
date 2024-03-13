"""cofig file """
import os
from common.utils.logging_handler import Logger

# pylint: disable=unspecified-encoding

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT","gcp-classroom-dev")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
GCP_LEARNING_RESOURCE_BUCKET = os.getenv("GCP_LEARNING_RESOURCE_BUCKET")

SCOPES = [
  "https://www.googleapis.com/auth/cloud-platform",
  "https://www.googleapis.com/auth/cloud-platform.read-only",
  "https://www.googleapis.com/auth/devstorage.full_control",
  "https://www.googleapis.com/auth/devstorage.read_only",
  "https://www.googleapis.com/auth/devstorage.read_write",
]
try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as \
    ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
IS_DEVELOPMENT = bool(
  os.getenv("IS_DEVELOPMENT", "").lower() in ("True", "true"))
TITLE_SIMILARITY_CER_THRESHOLD = 0.2
TITLE_GENERATION_BATCH_SIZE = 16
PAYLOAD_FILE_SIZE = 83886080  # 80MB

SERVICES = {
    "title-generation": {
        "host": "title-generation",
        "port": 80
    },
    "extractive-summarization": {
        "host": "extractive-summarization",
        "port": 80
    },
    "triple-extraction": {
        "host": "triple-extraction",
        "port": 80
    }
}

REDIS_HOST = os.getenv("REDIS_HOST")

BATCH_JOB_LIMITS = {
  "cpu": "1500m",
  "memory": "2500Mi"
}
BATCH_JOB_REQUESTS = {
  "cpu": "500m",
  "memory": "1500Mi"
}

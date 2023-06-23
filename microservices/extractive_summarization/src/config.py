"""script for loading configuration."""
import os

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
PROJECT_ID = os.environ.get("PROJECT_ID", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

IS_DEVELOPMENT = bool(os.getenv("IS_DEVELOPMENT", "").lower() \
    in ("True", "true"))

API_BASE_URL = os.getenv("BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

MODEL_TYPE = os.getenv("MODEL_TYPE")

IS_CLOUD_LOGGING_ENABLED = bool(os.getenv
            ("IS_CLOUD_LOGGING_ENABLED", "true").lower() in ("true",))

SERVICES = {
    "extractive-summarization": {
        "host": "extractive-summarization",
        "port": 80
    },
    "paraphrasing-practice": {
        "host": "paraphrasing-practice",
        "port": 80
    }
}

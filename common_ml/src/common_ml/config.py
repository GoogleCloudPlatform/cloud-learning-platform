"""Config file for common ml modules"""
import os
import requests
from google.api_core.exceptions import ResourceExhausted


SERVICES = {
    "coref-resolution": {
             "host": "coref-resolution",
             "port": "80"
            },
    "const-parsing": {
        "host": "const-parsing",
        "port": "80"
    }
}

MODEL_NAME_SUMMARY = "t5-base"
MODEL_NAME_PARAPHRASE = "Vamsi/T5_Paraphrase_Paws"

LONG_SENT_THRESHOLD = 50
FEEDBACK_FACT_KEYBERT_THRESHOLD = {
    "high": 0.38,
    "low": 0.2
}

SPACY_MODEL_TYPE_BIO = "en_ner_bionlp13cg_md"
IS_CLOUD_LOGGING_ENABLED = bool(os.getenv
            ("IS_CLOUD_LOGGING_ENABLED", "true").lower() in ("true",))

SPACY_MODEL_TYPES = {
    "default": "en_core_web_lg",
    "bio": "en_ner_bionlp13cg_md"
}

DEFAULT_JOB_LIMITS = {
      "cpu": "3",
      "memory": "7000Mi"
    }
DEFAULT_JOB_REQUESTS = {
      "cpu": "2",
      "memory": "5000Mi"
    }
RETRY_EXCEPTIONS = (ConnectionError, ResourceExhausted,
    requests.exceptions.ConnectionError)
SPLIT_THRESHOLD = 9000

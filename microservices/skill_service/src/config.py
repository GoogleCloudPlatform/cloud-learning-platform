"""
  Skill service config file
"""
# pylint: disable=unspecified-encoding,invalid-name

import os
from common.utils.logging_handler import Logger
from schemas.error_schema import (UnauthorizedResponseModel,
                                  InternalServerErrorResponseModel,
                                  ValidationErrorResponseModel)
from typing_extensions import Literal

PORT = os.environ["PORT"] if os.environ.get("PORT") is not None else 80
GCP_PROJECT = os.environ.get("GCP_PROJECT", "")
os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
GCP_BUCKET = os.environ.get("GCP_BUCKET", "")

try:
  with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace","r",
            encoding="utf-8",errors="ignore") as \
    ns_file:
    namespace = ns_file.readline()
    JOB_NAMESPACE = namespace
except FileNotFoundError as e:
  JOB_NAMESPACE = "default"
  Logger.info("Namespace File not found, setting job namespace as default")

CONTAINER_NAME = os.getenv("CONTAINER_NAME")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/cloud-platform.read-only",
    "https://www.googleapis.com/auth/devstorage.full_control",
    "https://www.googleapis.com/auth/devstorage.read_only",
    "https://www.googleapis.com/auth/devstorage.read_write"
]

COLLECTION = os.getenv("COLLECTION")

API_BASE_URL = os.getenv("API_BASE_URL")

SERVICE_NAME = os.getenv("SERVICE_NAME")

NUM_CLUSTERS = 1

EMSI_AUTH_URL = "https://auth.emsicloud.com/connect/token"

CLIENT_ID = os.getenv("CLIENT_ID")

CLIENT_SECRET = os.getenv("CLIENT_SECRET")

EMSI_URL = ("https://emsiservices.com/skills/versions/latest/skills?fields="
            "id%2Cname%2Ctype%2CinfoUrl%2Ctags")

SKILL_GRAPH_LEVELS = ["domain", "sub_domain", "category", "competency", "skill"]
KNOWLEDGE_GRAPH_LEVELS = ["concepts", "sub_concepts", "learning_objectives",
  "learning_units", "learning_resources"]
#Pydantic Validations
ALLOWED_SKILLGRAPH_LEVELS = Literal["domain", "sub_domain", "category",
  "competency", "skill"]
ALLOWED_KNOWLEDGE_LEVELS = Literal["concepts", "sub_concepts",
  "learning_objectives", "learning_units", "learning_resources"]

ALLOWED_SOURCES_FOR_GENERIC_CSV_INGESTION = Literal["snhu", "emsi", "osn",
                                                    "credential_engine"]
UNIFIED_ALIGNMENT_JOB_TYPE = "unified_alignment"
EMSI_INGESTION_JOB_TYPE = "emsi_ingestion"
CSV_INGESTION_JOB_TYPE = "csv_ingestion"
CE_INGESTION_JOB_TYPE = "credential_engine_ingestion"
OSN_INGESTION_JOB_TYPE = "osn_ingestion"
GENERIC_CSV_INGESTION_JOB_TYPE = "generic_csv_ingestion"
POPULATE_SKILL_EMBEDDING_JOB_TYPE = "skill_embedding_db_update"
CREATE_KG_EMBEDDING_JOB_TYPE = "create_knowledge_graph_embedding"
POPULATE_KNOWLEDGE_EMBEDDING_JOB_TYPE = "knowledge_embedding_db_update"
ROLE_SKILL_MAPPING_JOB_TYPE = "role_skill_alignment"

# reranker ranks the results from a set of semantically similar results
# retrieved.
# If the reranker score crosses this threshold, then the document is
# semantically similar to the query.
RERANKER_THRESHOLD = 0.5
SKILL_PARSER_RERANKED_THRESHOLD = 0.2
# If the ratio (number of mapped children nodes)/(total number of child nodes)
# crosses this threshold, the parent node is semantically similar to the query.
RATIO_THRESHOLD = 0.5

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
MATCHING_ENGINE_BUCKET_NAME = os.getenv("MATCHING_ENGINE_BUCKET_NAME")

SERVICES = {"matching-engine": {"host": "matching-engine", "port": 80}}

# ANN service parameters
EMBEDDING_ENDPOINT_ID = os.getenv("EMBEDDING_ENDPOINT_ID", "").strip("\"")
EMBEDDINGS_DIMENSION = 768
APPROXIMATE_NEIGHBOR_COUNT = 50
DISTANCE_MEASURE_TYPE = "DOT_PRODUCT_DISTANCE"
LEAF_NODE_EMB_COUNT = 500
LEAF_NODES_TO_SEARCH_PRECENT = 70

BI_ENCODER_MODELS = {
    "SKILL_PARSING": "all-mpnet-base-v2",
    "SEARCH": "all-mpnet-base-v2",
    "SKILL_ALIGNMENT": "all-mpnet-base-v2",
    "SKILL_TO_PASSAGE": "msmarco-bert-base-dot-v5"
}

CROSS_ENCODER_MODELS = {
    "SKILL_PARSING": "cross-encoder/stsb-roberta-large",
    "SEARCH": "cross-encoder/ms-marco-MiniLM-L-12-v2",
    "SKILL_ALIGNMENT": "cross-encoder/ms-marco-MiniLM-L-12-v2",
    "SKILL_TO_PASSAGE": "cross-encoder/ms-marco-MiniLM-L-12-v2"
}

PAYLOAD_FILE_SIZE = 2097152 #2MB

ERROR_RESPONSES = {
    500: {
        "model": InternalServerErrorResponseModel
    },
    401: {
        "model": UnauthorizedResponseModel
    },
    422: {
        "model": ValidationErrorResponseModel
    }
}

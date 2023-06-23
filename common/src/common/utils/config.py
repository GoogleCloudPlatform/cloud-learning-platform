"""Config file for utils"""
import os

IS_CLOUD_LOGGING_ENABLED = bool(os.getenv
            ("IS_CLOUD_LOGGING_ENABLED", "true").lower() in ("true",))

DEFAULT_JOB_LIMITS = {
      "cpu": "3",
      "memory": "7000Mi"
    }
DEFAULT_JOB_REQUESTS = {
      "cpu": "2",
      "memory": "5000Mi"
    }

JOB_TYPES_WITH_PREDETERMINED_TITLES = [
    "unified_alignment",
    "course-ingestion",
    "skill_alignment",
    "emsi_ingestion",
    "csv_ingestion",
    "wgu_ingestion",
    "generic_csv_ingestion",
    "credential_engine_ingestion",
    "skill_embedding_db_update",
    "knowledge_embedding_db_update",
    "onet_role_ingestion",
    "role_skill_alignment",
    "learning_resource_ingestion",
    "course-ingestion_topic-tree",
    "course-ingestion_learning-units",
    "create_knowledge_graph_embedding",
    "deep-knowledge-tracing",
    "validate_and_upload_zip"
]

BATCH_JOB_FETCH_TIME = 24  # in hours

BATCH_JOB_PENDING_TIME_THRESHOLD = 10  # in minutes

GCLOUD_LOG_URL = "https://console.cloud.google.com/logs/query;" +\
"query=resource.type%3D%22k8s_container%22%0Aresource.labels." +\
"project_id%3D%22{GCP_PROJECT}%22%0Aresource.labels.location" +\
"%3D%22{GCP_ZONE}%22%0Aresource.labels.cluster_name%3D%22" +\
"{GKE_CLUSTER}%22%0Aresource.labels.namespace_name%3D%22" +\
"{SKAFFOLD_NAMESPACE}%22%0Alabels.k8s-pod%2Fapp%3D%22" +\
"{MICROSERVICE}%22%20severity%3E%3DDEFAULT;timeRange=" +\
"{INIT_TIMESTAMP}%2F{FINAL_TIMESTAMP}?project={GCP_PROJECT}"

SERVICES = {
  "authentication": {
    "host": "authentication",
    "port": 80
  }
}

STAFF_USERS = ["assessor", "instructor", "coach"]
EXTERNAL_USER_PROPERTY_PREFIX = os.getenv("EXTERNAL_USER_PROPERTY_PREFIX")

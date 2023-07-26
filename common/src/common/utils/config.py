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

"""Config file for utils"""

import os
from enum import Enum

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

JOB_TYPE_UNIFIED_ALIGNMENT = "unified_alignment"
JOB_TYPE_COURSE_INGESTION = "course-ingestion"
JOB_TYPE_SKILL_ALIGNMENT = "skill_alignment"
JOB_TYPE_EMSI_INGESTION = "emsi_ingestion"
JOB_TYPE_CSV_SKILL_INGESTION = "csv_ingestion"
JOB_TYPE_WGU_SKILL_INGESTION = "wgu_ingestion"
JOB_TYPE_CSV_INGESTION = "generic_csv_ingestion"
JOB_TYPE_CREDENTIAL_ENGINE_INGESTION = "credential_engine_ingestion"
JOB_TYPE_EMBEDDING_DB_UPDATE = "skill_embedding_db_update"
JOB_TYPE_KNOWLEDGE_EMBEDDING_DB_UPDATE = "knowledge_embedding_db_update"
JOB_TYPE_ONET_ROLE_INGESTION = "onet_role_ingestion"
JOB_TYPE_ROLE_SKILL_ALIGNMENT = "role_skill_alignment"
JOB_TYPE_LEARNING_RESOURCE_INGESTION = "learning_resource_ingestion"
JOB_TYPE_COURSE_INGESTION_TOPIC_TREE = "course-ingestion_topic-tree"
JOB_TYPE_COURSE_INGESTION_LEARNING_UNITS = "course-ingestion_learning-units"
JOB_TYPE_CREATE_KNOWLEDGE_GRAPH_EMBEDDING = "create_knowledge_graph_embedding"
JOB_TYPE_DEEP_KNOWLEDGE_TRACING = "deep-knowledge-tracing"
JOB_TYPE_VALIDATE_AND_UPLOAD_ZIP = "validate_and_upload_zip"
JOB_TYPE_QUERY_ENGINE_BUILD = "query_engine_build"

JOB_TYPES_WITH_PREDETERMINED_TITLES = [
    JOB_TYPE_UNIFIED_ALIGNMENT,
    JOB_TYPE_COURSE_INGESTION,
    JOB_TYPE_SKILL_ALIGNMENT,
    JOB_TYPE_EMSI_INGESTION,
    JOB_TYPE_CSV_SKILL_INGESTION,
    JOB_TYPE_WGU_SKILL_INGESTION,
    JOB_TYPE_CSV_INGESTION,
    JOB_TYPE_CREDENTIAL_ENGINE_INGESTION,
    JOB_TYPE_EMBEDDING_DB_UPDATE,
    JOB_TYPE_KNOWLEDGE_EMBEDDING_DB_UPDATE,
    JOB_TYPE_ONET_ROLE_INGESTION,
    JOB_TYPE_ROLE_SKILL_ALIGNMENT,
    JOB_TYPE_LEARNING_RESOURCE_INGESTION,
    JOB_TYPE_COURSE_INGESTION_TOPIC_TREE,
    JOB_TYPE_COURSE_INGESTION_LEARNING_UNITS,
    JOB_TYPE_CREATE_KNOWLEDGE_GRAPH_EMBEDDING,
    JOB_TYPE_DEEP_KNOWLEDGE_TRACING,
    JOB_TYPE_VALIDATE_AND_UPLOAD_ZIP,
    JOB_TYPE_QUERY_ENGINE_BUILD
]

class JobTypes(Enum):
  """
  Enum class for JobTypes, used for param validation
  in Jobs Service
  """
  JOB_TYPE_UNIFIED_ALIGNMENT = "unified_alignment"
  JOB_TYPE_COURSE_INGESTION = "course-ingestion"
  JOB_TYPE_SKILL_ALIGNMENT = "skill_alignment"
  JOB_TYPE_EMSI_INGESTION = "emsi_ingestion"
  JOB_TYPE_CSV_SKILL_INGESTION = "csv_ingestion"
  JOB_TYPE_WGU_SKILL_INGESTION = "wgu_ingestion"
  JOB_TYPE_CSV_INGESTION = "generic_csv_ingestion"
  JOB_TYPE_CREDENTIAL_ENGINE_INGESTION = "credential_engine_ingestion"
  JOB_TYPE_EMBEDDING_DB_UPDATE = "skill_embedding_db_update"
  JOB_TYPE_KNOWLEDGE_EMBEDDING_DB_UPDATE = "knowledge_embedding_db_update"
  JOB_TYPE_ONET_ROLE_INGESTION = "onet_role_ingestion"
  JOB_TYPE_ROLE_SKILL_ALIGNMENT = "role_skill_alignment"
  JOB_TYPE_LEARNING_RESOURCE_INGESTION = "learning_resource_ingestion"
  JOB_TYPE_COURSE_INGESTION_TOPIC_TREE = "course-ingestion_topic-tree"
  JOB_TYPE_COURSE_INGESTION_LEARNING_UNITS = "course-ingestion_learning-units"
  JOB_TYPE_CREATE_KNOWLEDGE_GRAPH_EMBEDDING = "create_knowledge_graph_embedding"
  JOB_TYPE_DEEP_KNOWLEDGE_TRACING = "deep-knowledge-tracing"
  JOB_TYPE_VALIDATE_AND_UPLOAD_ZIP = "validate_and_upload_zip"
  JOB_TYPE_QUERY_ENGINE_BUILD = "query_engine_build"


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

#!/bin/bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Reference script for running skaffold commands to create backend services for
# Cloud Learning Platform

# TODO: Set Project ID and other variables
export PROJECT_ID=<your-project-id>
export CLP_VERSION=<tag-version> # e.g. v2.0.0-beta25
export REGION=<your-region>
export ZONE=<your-zone>
export GCP_PROJECT=${PROJECT_ID}
export GIT_SHA=$(git rev-parse HEAD)
export SKAFFOLD_DEFAULT_REPO="gcr.io/${PROJECT_ID}"
export SKAFFOLD_BUILD_CONCURRENCY=0

pushd ~/ailearning-backend
git checkout "${CLP_VERSION}"

gcloud container clusters list --project "${PROJECT_ID}"
gcloud container clusters get-credentials "${PROJECT_ID}-${REGION}" --region "${REGION}" --project "${PROJECT_ID}"

cd utils/firebase_indexing
PYTHONPATH=../common/src python3 firestore_indexing_setup.py
cd ../..

KEY_NAME=$(gcloud alpha services api-keys list \
  --filter="displayName='Browser key (auto created by Firebase)'" --format="value(name)")
echo "Key Name = ${KEY_NAME}"
export FIREBASE_API_KEY=$(gcloud alpha services api-keys get-key-string "${KEY_NAME}" --format="value(keyString)")
echo ${FIREBASE_API_KEY}
export BACKEND_API=https://${PROJECT_ID}-api.cloudpssolutions.com

API_KEY_DISPLAY_NAME="knowledge-graph-api-key"
gcloud alpha services api-keys create --display-name=${API_KEY_DISPLAY_NAME} --api-target="service=kgsearch.googleapis.com"
KEY_NAME=$(gcloud alpha services api-keys list --filter="displayName='${API_KEY_DISPLAY_NAME}'" --format="value(name)")
export KGS_API_KEY=$(gcloud alpha services api-keys get-key-string "${KEY_NAME}" --format="value(keyString)")
echo "${KGS_API_KEY}" | gcloud secrets versions add "google-kg-api-key" --data-file=-

export IS_DEVELOPMENT=false
export GENERATED_ASSESSMENTS_PATH=gs://${PROJECT_ID}/assessment_items
export TITLE_GENERATION_SAVED_MODEL_PATH=gs://${PROJECT_ID}/ml-models/title-generation/blooms/1637763009_pt
export TRIPLE_EXTRACTION_SAVED_MODEL_PATH=gs://${PROJECT_ID}/ml-models/triple-generation/checkpoints/models
export DIALOG_SYSTEMS_KG_DATA_DEV_PATH=gs://${PROJECT_ID}/knowledge-graph
export SAVED_MODEL=distilbert-pretraining/distilbert_base_uncased/distilbert_LM_training/saved_model/saved_model_epoch_3
export MWP_TFSERVING_MODEL_BASE_PATH=gs://${PROJECT_ID}/ml-models/hugging-face-checkpoints/${SAVED_MODEL}
export PE_TFSERVING_MODEL_BASE_PATH=gs://${PROJECT_ID}/ml-models/hugging-face-checkpoints/bert-base-cased-128/
export DKT_MODEL_WEIGHTS_PATH=gs://${PROJECT_ID}/ml-models/dkt
export NLU_CONFIG_PATH=gs://${PROJECT_ID}/knowledge-graph
export GCP_LEARNING_RESOURCE_BUCKET=${PROJECT_ID}
export DISABLE_MULTIHOP=true
export TUTOR_NAME=Thoreau
export IS_DIALOG_FLOW_SELECTION_REQUIRED=true
export ENABLE_DISPLAY_CONTEXT_FOR_AAQ=false
export IS_CLOUD_LOGGING_ENABLED=true
export RELEASE_VERSION=${CLP_VERSION}

skaffold run -p custom --default-repo=gcr.io/${PROJECT_ID} -l commit="${GIT_SHA}" -m v3_backends --tag=${CLP_VERSION}

popd

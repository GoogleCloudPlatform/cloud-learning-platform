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
export CLP_VERSION=<tag-version> # e.g. v3.0.0-beta25
export REGION=<your-region>
export ZONE=<your-zone>
export GCP_PROJECT=${PROJECT_ID}
export GIT_SHA=$(git rev-parse HEAD)
export SKAFFOLD_DEFAULT_REPO="gcr.io/${PROJECT_ID}"
export SKAFFOLD_BUILD_CONCURRENCY=0

pushd ~/cloud-learning-platform
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

export IS_DEVELOPMENT=false
export IS_CLOUD_LOGGING_ENABLED=true
export RELEASE_VERSION=${CLP_VERSION}

skaffold run -p custom --default-repo=gcr.io/${PROJECT_ID} -l commit="${GIT_SHA}" -m v3_backends --tag=${CLP_VERSION}

popd

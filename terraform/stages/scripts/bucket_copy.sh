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

# Script to copy sample data from gs://aitutor-dev to current project bucket

export ML_BUCKET=aitutor-dev
export FIRESTORE_BUCKET=aitutor-dev
export FIRESTORE_DEMO_FOLDER=Oct_20_2022_Demo_Course
mkdir bucket_copy
mkdir bucket_copy/ml-models
mkdir bucket_copy/knowledge-graph
mkdir bucket_copy/course-resources
mkdir -p bucket_copy/firestore-export/${FIRESTORE_DEMO_FOLDER}

# Copy sample data from aitutor-dev buckets to local
gcloud auth login # google account
gsutil -m cp -r gs://${ML_BUCKET}/ml-models/*        bucket_copy/ml-models
gsutil -m cp -r gs://${ML_BUCKET}/knowledge-graph/*  bucket_copy/knowledge-graph
gsutil -m cp -r gs://${ML_BUCKET}/course-resources/* bucket_copy/course-resources
gsutil -m cp -r gs://${FIRESTORE_BUCKET}/firestore-export/${FIRESTORE_DEMO_FOLDER}/* \
  bucket_copy/firestore-export/${FIRESTORE_DEMO_FOLDER}/

# Copy sample data from local to the project bucket
gcloud auth login # altostrat/project account, if different
gsutil -m cp -r bucket_copy/* gs://"${PROJECT_ID}"

gcloud firestore import gs://"${PROJECT_ID}/firestore-export/${FIRESTORE_DEMO_FOLDER}"

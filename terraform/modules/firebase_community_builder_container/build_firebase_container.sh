#!/usr/bin/env bash
set -eo pipefail

export GCP_APPLICATION=firebase-community-builder-image
export TAG_VERSION=v0.0.1

echo "DOWNLOAD THE CLOUD BUILDER REPOSITORY"
rm -rf cloud-builders-community
git clone https://github.com/GoogleCloudPlatform/cloud-builders-community.git

echo "NAVIGATE TO THE FIREBASE BUILDER IMAGE"
cd cloud-builders-community/firebase

echo "SUBMIT THE BUILDER TO YOUR PROJECT"
gcloud builds submit . --project="${PROJECT_ID}" --quiet --tag "gcr.io/${PROJECT_ID}/$GCP_APPLICATION:$TAG_VERSION"

echo "CLEANUP THE ROOT FOLDER"
cd ../.. && rm -rf cloud-builders-community

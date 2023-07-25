# Copyright 2022 Google LLC
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

# Hardcoded the project ID for all local development.
declare -a EnvVars=(
  "PROJECT_ID"
  "SKAFFOLD_NAMESPACE"
  "REGION"
)
for variable in ${EnvVars[@]}; do
  if [[ -z "${!variable}" ]]; then
    printf "$variable is not set.\n"
    exit -1
  fi
done

CLUSTER_NAME=core-learning-services-dev-us-central1
EXPECTED_CONTEXT=gke_${PROJECT_ID}_${REGION}_${CLUSTER_NAME}

BLUE=$(tput setaf 4)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
echo
echo "PROJECT_ID=${PROJECT_ID}"
echo "SKAFFOLD_NAMESPACE=${SKAFFOLD_NAMESPACE}"
echo "REGION=${REGION}"
echo


init() {
  printf "\n${BLUE}Switch gcloud config to project ${PROJECT_ID} ${NORMAL}\n"
  EXISTING_PROJECT_ID=`gcloud projects list --filter ${PROJECT_ID} | grep ${PROJECT_ID}`
  if [[ "$EXISTING_PROJECT_ID" == "" ]]; then
    printf "Project ${PROJECT_ID} doesn't exist or you don't have access.\n"
    printf "Terminated.\n"
    exit 0
  else
    printf "Project ${PROJECT_ID} found.\n"
  fi

  gcloud config set project $PROJECT_ID

  printf "\n${BLUE}Set up gcloud and kubectl context ...${NORMAL}\n"
  gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${REGION} --project ${PROJECT_ID}
}

setup_namespace() {
  printf "\n${BLUE}Creating namespace: ${SKAFFOLD_NAMESPACE} ...${NORMAL}\n"
  kubectl create ns $SKAFFOLD_NAMESPACE

  printf "\n${BLUE}Using namespace ${SKAFFOLD_NAMESPACE} for all kubectl operations ...${NORMAL}\n"
  kubectl config set-context --current --namespace=$SKAFFOLD_NAMESPACE

  printf "\n${BLUE}Verifying the kubectl context name ...${NORMAL}\n"
  CURRENT_CONTEXT=`kubectl config current-context`
  if [[ "$CURRENT_CONTEXT" = "$EXPECTED_CONTEXT" ]]; then
    printf "OK.\n"
  else
    printf "${RED}Expecting kubectl context as "${EXPECTED_CONTEXT}" but got "${CURRENT_CONTEXT}". ${NORMAL}\n"
  fi
}

add_service_account_key() {
  SA_ACCOUNT_ID=$1

  printf "\n${BLUE}Adding Service Account '$SA_ACCOUNT_ID' to cluster ...${NORMAL}\n"

  declare EXISTING_SECRET=`kubectl get secrets -n $SKAFFOLD_NAMESPACE | grep "$SA_ACCOUNT_ID-sa-key"`
  if [[ "$EXISTING_SECRET" != "" ]]; then
    printf "Removing previous created secret '$SA_ACCOUNT_ID-sa-key' in namespace $SKAFFOLD_NAMESPACE.\n"
    kubectl delete secret $SA_ACCOUNT_ID-sa-key -n $SKAFFOLD_NAMESPACE
  fi

  printf "\n${BLUE}Retrieving latest '$SA_ACCOUNT_ID-sa-key' from Secret Manager ...${NORMAL}\n"
  mkdir -p .tmp
  gcloud secrets versions access latest --secret "$SA_ACCOUNT_ID-sa-key" > ./.tmp/$PROJECT_ID-$SA_ACCOUNT_ID-sa-key.json

  printf "\n${BLUE}Adding Service Account key as '$SA_ACCOUNT_ID-sa-key' to cluster, namespace=$SKAFFOLD_NAMESPACE ...${NORMAL}\n"
  kubectl create secret generic $SA_ACCOUNT_ID-sa-key --from-file=./.tmp/${PROJECT_ID}-$SA_ACCOUNT_ID-sa-key.json --namespace=$SKAFFOLD_NAMESPACE

  printf "\n${BLUE}Service Account key added as '$SA_ACCOUNT_ID-sa-key' in cluster, namespace=$SKAFFOLD_NAMESPACE ...${NORMAL}\n"
  printf "Please make sure the key content is greater than 0 byte:\n"
  kubectl describe secrets $SA_ACCOUNT_ID-sa-key -n $SKAFFOLD_NAMESPACE | grep bytes

  rm ./.tmp/$PROJECT_ID-$SA_ACCOUNT_ID-sa-key.json
}

init
setup_namespace
add_service_account_key "signurl"

printf "\n${BLUE}Done. ${NORMAL}\n"

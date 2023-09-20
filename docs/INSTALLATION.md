# Cloud Learning Platform Installation

## 1. Prerequisites

### Access
- Access to the following Github repos:
    - [GoogleCloudPlatform/cloud-learning-platform](https://github.com/GoogleCloudPlatform/cloud-learning-platform)
- A new project for installation with Project Owner (`roles/owner`)
- A domain or sub_domain that you control and can create DNS records for (not needed for CEs)

### Quotas
You'll need the following quotas in your preferred zone
- 48 vCPU
- 4 x T4 GPUs

### Tools
Install the following tools:
- [gcloud](https://cloud.google.com/sdk/docs/install)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## 2. Project Bootstrap

Please make sure that you have the project `Owner` role to be able to update the organizational policies for CLP deployment. You will use a provided Terraform module to perform the following:
- Bootstrap a project in your organization
- Create a Terraform service account and Terraform state bucket in the project for further Terraform scripts

For "CLP version", use the branch or tag of the CLP version you are deploying.  If you aren't sure, use "main".

From your workstation:
```bash
export PROJECT_ID=<your-project-id>
export REGION=<your-region>
export ZONE=<your-zone>
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")

export CLP_VERSION=<clp_tag>
git clone https://github.com/GoogleCloudPlatform/cloud-learning-platform.git
cd cloud-learning-platform
git checkout $CLP_VERSION
cd terraform/stages/project_bootstrap/
```

Log in to your project:
```bash
gcloud auth login
```

You will need to also create ADC credentials pointed towards an org admin account for use by the Terraform client.
```bash
gcloud auth application-default login
```
And verify if they've taken:
```bash
cat ~/.config/gcloud/application_default_credentials.json
```

Set `gcloud` to point to your project (if not already)
```bash
gcloud config list
gcloud config set project ${PROJECT_ID}
```

Run the following to set Terraform variables:
```bash
# Pass variables to terraform using environment prefix TF_VAR_
export TF_VAR_project_id=${PROJECT_ID}
export TF_VAR_region=${REGION}
export TF_VAR_zone=${ZONE}
export TF_VAR_bucket_region_or_multiregion="US"
```

Now that you're logged in, initialize and run a `terraform apply` command to see the expected changes. Inspect the changes before typing `yes` when prompted.
```commandline
terraform init
terraform apply
```

Ensure that a bucket with the same name as the project has been created:
```commandline
gsutil ls -p "${PROJECT_ID}"
```

There should also be a jump host VM in the project:
```commandline
gcloud compute instances list
```

###  Summary
In this section you successfully created the following:
- A bucket to capture future terraform state and prepare for CI/CD
- A Terraform service account with the required permissions
- A jump host to perform the rest of the installation

## 3. Main Infrastructure Installation - GKE Cluster

### Copy bootstrap terraform state to tfstate-bucket
```bash
gsutil cp ../project_bootstrap/terraform.tfstate gs://"${PROJECT_ID}"-tfstate/env/bootstrap/terraform.tfstate
```

### Enable deletion protection for the jump host
```bash
gcloud compute instances update jump-host --deletion-protection --project="${PROJECT_ID}" " --zone=${ZONE}
```

### SCP startup script to jump host
```bash
gcloud compute scp ../scripts/bastion_startup.sh jump-host:~ --zone=${ZONE} --tunnel-through-iap --project="${PROJECT_ID}"
```

### Log onto the jump host using IAP and start tmux
```bash
gcloud compute ssh jump-host --zone=${ZONE} --tunnel-through-iap --project=${PROJECT_ID}
```

### Run the startup script (takes 10-20 min)
```bash
source ~/bastion_startup.sh
```

### Start tmux on the jump host
Preferred so that disconnected sessions are not lost (https://tmuxcheatsheet.com/). To re-connect `tmux attach`
```bash
tmux
```

### Git Clone CLP repos
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git config --global credential.https://github.com.username "username"

git config --global credential.helper store
git clone https://github.com/GoogleCloudPlatform/cloud-learning-platform.git
```

### Set Project ID and other variables
For "CLP version", use the branch or tag of the CLP version you are deploying.  If you aren't sure, use "main".

```bash
export PROJECT_ID=<your-project-id>
export LDAP=<your-ldap>
export GITHUB_ID=<your-github-id>
export REGION=<your-region>
export ZONE=<your-zone>
export CLP_VERSION=<clp-version>
```

### Authenticate to Google Cloud
```bash
gcloud auth login
gcloud auth application-default login
```

### Create and download service key for terraform account
This account is used for several reasons:
- Ensuring a consistent experience, as users coming to this process may have varying permissions
- Creating Firebase resources in Terraform requires the use of a Service Account because of [API limitations](https://github.com/hashicorp/terraform-provider-google/issues/8287)
- Setting up CI/CD for this project to consume upstream changes is halfway done for you
```bash
export SA_KEY_FILE=~/clp-terraform-cicd-key.json
gcloud iam service-accounts keys create ${SA_KEY_FILE} \
--iam-account=terraform-cicd@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=${SA_KEY_FILE}
```

### Define input variables for Terraform
```bash
export TF_VAR_project_id=${PROJECT_ID}
export TF_VAR_region=${REGION}
export TF_VAR_firestore_region="us-central"
export TF_VAR_gke_cluster_zones=${ZONE}
export TF_VAR_github_owner=${GITHUB_ID}
export TF_VAR_api_domain="${PROJECT_ID}-api"
export TF_VAR_web_app_domain="${PROJECT_ID}"
export TF_VAR_ckt_app_domain="${PROJECT_ID}-ckt"
export TF_VAR_github_ref="refs/tags/${CLP_VERSION}"
```

### Set up the frontend app domains and whitelisted users
These variables have been defaulted for Argolis projects
```bash
export TF_VAR_cert_issuer_email="${LDAP}@google.com"
export TF_VAR_org_domain_name="${LDAP}.altostrat.com"
export TF_VAR_base_domain="cloudpssolutions.com"
export TF_VAR_ai_tutor_whitelist_domains="google.com"
export TF_VAR_ai_tutor_whitelist_emails="${LDAP}@google.com,admin@${LDAP}.altostrat.com"
export TF_VAR_ckt_whitelist_domains="google.com"
export TF_VAR_ckt_whitelist_emails="${LDAP}@google.com,admin@${LDAP}.altostrat.com"
```

### Terraform Module Initialization
Now change directories to `demo_environment` and initialize the terraform module,
```bash
pushd cloud-learning-platform
git checkout "${CLP_VERSION}"
cd terraform/stages/demo_environment

terraform init -backend-config="bucket=${PROJECT_ID}-tfstate"
terraform plan | grep -e "#"
# Firestore may only be initialized once
FIRESTORE_INIT="-var=firebase_init=false"
if [[ $(gcloud alpha firestore databases list --project="${PROJECT_ID}" --quiet | grep -c uid) == 0 ]]; then
  FIRESTORE_INIT="-var=firebase_init=true"
fi

terraform apply ${FIRESTORE_INIT} --auto-approve
popd
```

### Summary
In this section you successfully created the following via Terraform
- Firebase Base Apps
- GKE Cluster for backends and GCS buckets
- Ingress and other Service Accounts and Secrets on the Cluster

## 4. Firebase Setup

Follow [Firebase setup Instructions](FIREBASE.md)

### Firestore Index Creation
Checkout the backend repo and select the latest release version you'd like to deploy to match the frontends you just deployed.
Deploy the needed indexes to firestore. Make sure the database import is completed first.
```bash
cd cloud-learning-platform
export PWD=$(pwd)
export GCP_PROJECT=${PROJECT_ID}
echo "Your current GCP Project ID is: "${GCP_PROJECT}

cd utils
PYTHONPATH=../common/src python firestore_indexing.py
cd ..
```

## 5. GKE Backend Deployment

We will now run a series of `skaffold` commands to build the necessary containers in cloud build and deploy them to the GKE cluster to power the backend services.

First connect to your GKE cluster that you've already provisioned. You can find the command here.
<img src="docs/static/images/gke_credentials.png" width=70%>

```bash
gcloud container clusters get-credentials ${GCP_PROJECT}-${REGION} --region ${REGION} --project ${GCP_PROJECT}
```

[kubectx and kubens](https://github.com/ahmetb/kubectx) are handy tools to easily switch between Kubernetes clusters and namespaces.

Return to the repo root. Make sure you have the version you desire checked out.
```bash
cd $PWD
echo "Your current GCP Project ID is: "$(git branch --show-current)

export GCP_PROJECT=${PROJECT_ID}
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
echo "Your current GCP Project ID is: "${PROJECT_ID}

export BACKEND_API=https://$PROJECT_ID-api.cloudpssolutions.com
# GIT_RELEASE=$(git describe --tags --abbrev=0 --exact-match)
GIT_SHA=$(git rev-parse HEAD)
```

Run the following to get Firebase API key (Web API key):
```bash
KEY_NAME=$(gcloud alpha services api-keys list --filter="displayName='Browser key (auto created by Firebase)'" --format="value(name)")
export FIREBASE_API_KEY=$(gcloud alpha services api-keys get-key-string ${KEY_NAME} --format="value(keyString)")
```

Set environment variables:
```bash
export IS_DEVELOPMENT=false
export IS_CLOUD_LOGGING_ENABLED=true
export RELEASE_VERSION=${CLP_VERSION}
export SKAFFOLD_BUILD_CONCURRENCY=0
```

Deploy each set of services, one set at a time. This can take several tries due to transient build failures. These can take over 10 minutes to complete.

> **_NOTE:_** Make sure `gcloud` is set to the proper project and your Kubeconfig is set to the appropriate cluster. Make sure your user account is also set as Application Default Credentials so `skaffold` and `helm` have the appropriate access.

You can watch the logs of your builds in [Cloud Build](https://console.cloud.google.com/cloud-build/builds) as well as streaming to your command line.
```bash
echo ${GCP_PROJECT} ${PROJECT_ID} ${GIT_SHA} ${CLP_VERSiON}
# Deploy backend microservices
skaffold run -p custom --default-repo=gcr.io/${PROJECT_ID} -l commit=${GIT_SHA} -m v3_backends --tag ${CLP_VERSION}
```

Eventually you should see that all the containers are built and `skaffold` is starting to deploy resources.
You can also watch the pods deploy by running this in another terminal session:
```bash
kubectl get po

# or if you have `watch`
watch kubectl get po
```

Eventually you will see the deployments stabilize:

## 6. Scaling the cluster

To save on cost it may be desirable to reduce GCP spend when the application is not being used or evaluated. Primarily this is achieved by turning down the GKE cluster and turning off the backend. Please not this pathway is only somewhat tested. You should test your user journeys each time you turn up the cluster.

### Turning Down

1. For each node pool in the console:
  - Disable auto scaling, Click Save
  - Set nodes = 0, Click Save

### Turning Up

1. Turn on Auto-scaling for both pools (min 1, max 8)
2. Change number of nodes for both pools to 1-4 (autoscaler will even it out)
3. Let all services turn on

Use `kubectl get pods` to monitor the status of pods.
`ContainerCreating` means it’s starting, `Pending` meaning it is waiting for resources, i.e. GPU node

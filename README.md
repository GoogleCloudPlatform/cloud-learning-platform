# Cloud Learning Platform

<!-- vscode-markdown-toc -->
* 1. [Overview](#Overview)
	* 1.1. [What is Cloud Learning Platform (“CLP”)](#WhatisCloudLearningPlatformCLP)
	* 1.2. [Why CLP?](#WhyCLP)
	* 1.3. [High-level Architecture Overview](#High-levelArchitectureOverview)
	* 1.4. [Services Highlights](#ServicesHighlights)
	* 1.5. [Vision and Roadmap](#VisionandRoadmap)
* 2. [Getting Started](#GettingStarted)
	* 2.1. [Prerequisites](#Prerequisites)
	* 2.2. [GCP Organizational policies](#GCPOrganizationalpolicies)
	* 2.3. [GCP Foundation Setup - Terraform](#GCPFoundationSetup-Terraform)
	* 2.4. [Deploying Kubernetes Microservices to GKE](#DeployingKubernetesMicroservicestoGKE)
	* 2.5. [Deploying Microservices to CloudRun](#DeployingMicroservicestoCloudRun)
* 3. [Development](#Development)
* 4. [End-to-End API tests](#End-to-EndAPItests)
* 5. [CI/CD and Test Automation](#CICDandTestAutomation)
	* 5.1. [Github Actions](#GithubActions)
	* 5.2. [Test Github Action workflows locally](#TestGithubActionworkflowslocally)
* 6. [CloudBuild](#CloudBuild)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

> This solution skeleton is created from https://github.com/GoogleCloudPlatform/solutions-template

Please contact jonchen@google.com for any questions.

##  1. <a name='Overview'></a>Overview

###  1.1. <a name='WhatisCloudLearningPlatformCLP'></a>What is Cloud Learning Platform (“CLP”)

Cloud Learning Platform is a collection of core services and data models intended to provide the educationally-specific infrastructure for any e-learning ecosystem,  whether K-12, Higher Ed, or Continuing/Professional Education.

These services are turned up in a Kubernetes instance for scalability and management; which also therefore assure the ownership of the data remains fully  in the control of the teaching organization.

CLP has no user surfaces; these are to be integrated (in the case of existing edtech products) or custom built  (a build which is now a very thin UX later, where the CLP services are doing much of the heavy lifting).    The UX, workflow, branding, etc is therefore also fully in control of the teaching organization;   and it  will be possible to make lightweight surfaces for any and all users as desired.

###  1.2. <a name='WhyCLP'></a>Why CLP?

The most significant challenge currently in e-learning is the siloed nature of the architecture.  Often 5-400 different systems are involved, and very few speak to each other; even fewer speak to each other at the right grain size.  Therefore the goals of CLP are, among others, to:

- Enable all data about the student learning journey to be managed in a central data bus
- Collect + make available data at the right grain size (skills + knowledge) for competency-based learning
- Connect learning all the way through to job skills (and understand the latter)
- Use this data to drive the right AI services to drive AI appropriately for education – not just for personalized student experiences, but also for teachers (knowing the level of the course) and instructional designers (how to create materials for specific skills)

###  1.3. <a name='High-levelArchitectureOverview'></a>High-level Architecture Overview

![Alt text](.github/assets/highlevel_architecture.png)


###  1.4. <a name='ServicesHighlights'></a>Services Highlights

- **Credential Pathway Service** - Offer pathways from existing credentials to higher-level credentials that can be achieved in a given order in a given number of steps
- **Student Mastery Model** service using Deep Knowledge tracing or Item Repsonse Theory  - Offer a variety of methods   of establishing student mastery of specific skills
- **Learning Record Store** - Takes data from any number of sources to track student progress for nudging / research / reporting purposes

###  1.5. <a name='VisionandRoadmap'></a>Vision and Roadmap

The vision of CLP is to offer a complete services and data layer,  to manage the movement of data to and from all systems in an educational ecosystem, as well as using that data to drive improved outcomes and support,  better reporting, and most importantly better use of AI tools.

In Q3/Q4  2023 our intention is to
- release updates to the knowledge extraction and assessment generation services with improved AI models;   which will include video and image question prompts and responses; as well as “higher order” (vis-a-vis Bloom’s taxonomy) problem solving
- introduce an AI orchestration service to integrate with any and all AI tools that may be relevant to a student or teacher experience
- enable course ingestion of Common Cartridge and HTML documents
- add services for faculty to generate course content, syllabi, and lesson plans
- integrate CLP services into Google Workspace/Classroom

In Q1/Q2 2024, our intention is to
- add services to handle the marketing and enrollment workflow
- add services to enable faculty to create exercises and additional content on the fly, adapted to the skill level of students in their particular section
- add service to grade large numbers of open-ended questions which cannot be fully machine graded, by bucketing similar answers and asking assessors to grade those buckets

##  2. <a name='GettingStarted'></a>Getting Started

This guide will detail how to set up your new solutions template project. See the [development guide](./DEVELOPMENT.md) for how to contribute to the project.

###  2.1. <a name='Prerequisites'></a>Prerequisites

Project Requirements

| Tool      | Current Version |
| --------- | --------------- |
| Python    | v3.9            |
| Skaffold  | v1.39.2         |
| GKE       | v1.22           |
| Kustomize | v4.3.1          |

```
# Set up environmental variables
export PROJECT_ID=core-learning-services-dev
export ADMIN_EMAIL=dhodun@google.com
export CLASSROOM_ADMIN_EMAIL=lms_admin_teacher@dhodun.altostrat.com
export REGION=us-central1
export API_DOMAIN=cloudpssolutions.com
export BASE_DIR=$(pwd)

# Login to Google Cloud
gcloud auth application-default login
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set project $PROJECT_ID
```

For development with Kubernetes on GKE:

Install required packages:

- For MacOS:

  ```
  brew install --cask skaffold kustomize google-cloud-sdk
  ```

- For Windows:

  ```
  choco install -y skaffold kustomize gcloudsdk
  ```

- For Linux/Ubuntu:
  ```
  curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
  sudo install skaffold /usr/local/bin/
  ```

* Make sure to use **skaffold 1.24.1** or later for development.

###  2.2. <a name='GCPOrganizationalpolicies'></a>GCP Organizational policies

Optionally, you may need to update Organization policies for CI/CD test automation.

Run the following commands to update Organization policies:

```
export ORGANIZATION_ID=$(gcloud organizations list --format="value(name)")
gcloud resource-manager org-policies disable-enforce constraints/compute.requireOsLogin --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/compute.vmExternalIpAccess --organization=$ORGANIZATION_ID
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --organization=$ORGANIZATION_ID
```

Or, change the following Organization policy constraints in [GCP Console](https://console.cloud.google.com/iam-admin/orgpolicies)

- constraints/compute.requireOsLogin - Enforced Off
- constraints/compute.vmExternalIpAccess - Allow All

###  2.3. <a name='GCPFoundationSetup-Terraform'></a>GCP Foundation Setup - Terraform

Set up Terraform environment variables and GCS bucket for state file.
If the new project is just created recently, you may need to wait for 1-2 minutes
before running the Terraform command.

```
export TF_VAR_project_id=$PROJECT_ID
export TF_VAR_api_domain=$API_DOMAIN
export TF_VAR_web_app_domain=$API_DOMAIN
export TF_VAR_admin_email=$ADMIN_EMAIL
export TF_BUCKET_NAME="${PROJECT_ID}-tfstate"
export TF_BUCKET_LOCATION="us"

# Grant Storage admin to the current user IAM.
export CURRENT_USER=$(gcloud config list account --format "value(core.account)")
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$CURRENT_USER" --role='roles/storage.admin'

# Create Terraform Statefile in GCS bucket.
bash setup/setup_terraform.sh
```

Run Terraform apply

```
cd terraform/environments/dev
terraform init -backend-config=bucket=$TF_BUCKET_NAME

# Enabling GCP services first.
terraform apply -target=module.project_services -target=module.service_accounts -auto-approve

# Run the rest of Terraform
terraform apply -auto-approve
```

###  2.4. <a name='DeployingKubernetesMicroservicestoGKE'></a>Deploying Kubernetes Microservices to GKE

Connect to the `default-cluster`:

```
gcloud container clusters get-credentials core-learning-services-dev-us-central1 --region $REGION --project $PROJECT_ID
```

Build all microservices (including web app) and deploy to the cluster:

```
cd $BASE_DIR
skaffold run -p prod --default-repo=gcr.io/$PROJECT_ID
```

Test with API endpoint:

```
export API_DOMAIN=$(kubectl describe ingress | grep Address | awk '{print $2}')
echo "http://${API_DOMAIN}/lms/docs"
```

###  2.5. <a name='DeployingMicroservicestoCloudRun'></a>Deploying Microservices to CloudRun

Build common image

```
cd common
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="common"
```

Set up endpoint permission:

```
export SERVICE_NAME=lms
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

Build service image

```
gcloud builds submit --config=cloudbuild.yaml --substitutions=\
_CLOUD_RUN_SERVICE_NAME=$SERVICE_NAME,\
_PROJECT_ID="$PROJECT_ID",\
_REGION="$REGION",\
_REPOSITORY="cloudrun",\
_IMAGE="cloudrun-sample",\
_SERVICE_ACCOUNT="deployment-dev@$PROJECT_ID.iam.gserviceaccount.com",\
_ALLOW_UNAUTHENTICATED_FLAG="--allow-unauthenticated"
```

Manually deploy a microservice to CloudRun with public endpoint:

```
gcloud run services add-iam-policy-binding $SERVICE_NAME \
--region="$REGION" \
--member="allUsers" \
--role="roles/run.invoker"
```

##  3. <a name='Development'></a>Development

##  4. <a name='End-to-EndAPItests'></a>End-to-End API tests

TBD

##  5. <a name='CICDandTestAutomation'></a>CI/CD and Test Automation

###  5.1. <a name='GithubActions'></a>Github Actions

###  5.2. <a name='TestGithubActionworkflowslocally'></a>Test Github Action workflows locally

- Install Docker desktop: https://www.docker.com/products/docker-desktop/
- Install [Act](https://github.com/nektos/act)

  ```
  # Mac
  brew install act

  # Windows
  choco install act-cli
  ```

- Run a specific Workflow
  ```
  act --workflows .github/workflows/e2e_gke_api_test.yaml
  ```

##  6. <a name='CloudBuild'></a>CloudBuild

TBD

# Development Process & Best Practices

See the [developer guide](./DEVELOPMENT.md) for detailed development workflow

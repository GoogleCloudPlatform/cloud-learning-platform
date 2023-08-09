# Project setting variables
variable "project_id" {
  type        = string
  description = "GCP Project ID"

  validation {
    condition     = length(var.project_id) > 0
    error_message = "The project_id value must be an non-empty string."
  }
}

variable "region" {
  type        = string
  description = "GCP Region"
  validation {
    condition     = length(var.region) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "bucket_region_or_multiregion" {
  type        = string
  description = "GCP Region or Multiregion"
  validation {
    condition     = length(var.bucket_region_or_multiregion) > 0
    error_message = "The region value must be an non-empty string."
  }
}

variable "firestore_region" {
  type        = string
  description = "Firestore Region - must be app_engine region"
  # options for firestore: https://cloud.google.com/appengine/docs/locations
  # us-central1 and europe-west1 must be us-central and europe-west for legacy reasons
}

variable "multiregion" {
  type        = string
  description = "multiregion location"
  default     = "us"
}

variable "env" {
  type        = string
  description = "specify the Cloud environment"
  default     = "dev"
}

variable "github_owner" {
  type        = string
  description = "Your github username (or github org if enterprise deployment)"
  default     = "GPS-Solutions"
}


# custom vpc network variables
variable "vpc_network" {
  type        = string
  description = "specify the vpc name"
  default     = "vpc-01"
}


# GKE private cluster variables
variable "gke_cluster_zones" {
  type        = list(string)
  description = "specify the zones for the cluster region"
}

variable "master_authorized_networks" {
  type        = list(object({ cidr_block = string, display_name = string }))
  description = "List of master authorized networks. If none are provided, disallow external access (except the cluster node IPs, which GKE automatically whitelists)."
  default = [{
    cidr_block   = "0.0.0.0/0"
    display_name = "all-IPs"
  }, ]
}

variable "network" {
  type        = string
  description = "VPC network to host the gke cluster"
  default     = "vpc-01"
}

variable "subnetwork" {
  type        = string
  description = "VPC subnetwork which will be used by the cluster"
  default     = "vpc-01-subnet-01"
}

variable "ip_range_pods" {
  type        = string
  description = "The name of the secondary subnet ip range to use for pods"
  default     = "secondary-pod-range-01"
}

variable "ip_range_services" {
  type        = string
  description = "The name of the secondary subnet range to use for services"
  default     = "secondary-service-range-01"
}

variable "network_project_id" {
  type        = string
  description = "The project ID of the shared VPC's host (for shared vpc support)"
  default     = null
}

variable "github_ref" {
  type        = string
  description = "Github ref to use for cloud build triggers"
  default     = "refs/tags/v2.0.0-beta12.7-demo"
}

# GKE deployments variables
variable "cert_issuer_email" {
  type        = string
  description = "email of the cert issuer"
}

variable "base_domain" {
  type        = string
  description = "base domain or subdomain for firebase and APIs"
}

# Firebase Module variables
variable "ai_tutor_whitelist_domains" {
  type        = string
  description = "Comma separated list of email domains that should have access to AI Tutor"
}

variable "ai_tutor_whitelist_emails" {
  type        = string
  description = "Comma separated list of individual emails that should have access to AI Tutor"
}

variable "ckt_whitelist_domains" {
  type        = string
  description = "Comma separated list of email domains that should have access to CKT"
}

variable "ckt_whitelist_emails" {
  type        = string
  description = "Comma separated list of individual emails that should have access to CKT"
}

variable "gpu_np_max_count" {
  type        = string
  description = "Max node pool count for auto scaling (0 to disable GPU nodes)"
  default     = "6"
}

variable "existing_custom_vpc" {
  type        = bool
  description = "custom vpc created by the clients/users(manually) True/False"
  default     = false
}

variable "max_pods_per_node" {
  type        = string
  description = "Maximun pods to be assigned to the nodes"
  default     = "110"
}

variable "datapath_provider" {
  type        = string
  description = "The desired datapath provider for this cluster. By default, DATAPATH_PROVIDER_UNSPECIFIED enables the IPTables-based kube-proxy implementation. ADVANCED_DATAPATH enables Dataplane-V2 feature."
  default     = "ADVANCED_DATAPATH"
}

variable "enable_vertical_pod_autoscaling" {
  type        = bool
  description = "Vertical Pod Autoscaling automatically adjusts the resources of pods controlled by it"
  default     = true
}

variable "release_channel" {
  type        = string
  description = "The release channel of this cluster. Accepted values are UNSPECIFIED, RAPID, REGULAR and STABLE. Defaults to UNSPECIFIED."
  default     = "REGULAR"
}

variable "enable_shielded_nodes" {
  type        = bool
  description = "Enable Shielded Nodes features on all nodes in this cluster"
  default     = true
}

variable "web_app_domain" {
  type        = string
  description = "Subdomain name for frontend of Aitutor application"
  default     = null
}

variable "ckt_app_domain" {
  type        = string
  description = "Subdomain name for frontend of CKT application"
  default     = null
}

variable "api_domain" {
  type        = string
  description = "Subdomain name for backend"
  default     = null
}

variable "gclb_api_domain" {
  type        = string
  description = "Subdomain name for backend, GCLB version"
  default     = null
}

variable "node_pools_create_before_destroy" {
  type        = bool
  description = "Enable Shielded Nodes features on all nodes in this cluster"
  default     = true
}

variable "enable_secret_manager_secret_version_creation" {
  type        = bool
  description = "Enable Secret Manager Secret Version Creation"
  default     = true
}

variable "enable_signurl_key_rotation" {
  type        = bool
  description = "Enable SignURL Key Rotation"
  default     = true
}

variable "enable_service_account_key_creation" {
  type        = bool
  description = "Enable Service Account Key Creation"
  default     = true
}

variable "enable_kubernetes_secret_creation" {
  type        = bool
  description = "Enable Kubernetes Secret Creation"
  default     = true
}

variable "enable_certman_gcr_io_images" {
  type        = bool
  default     = false
  description = "Enabling this to use cert-manager images from the gcr.io/google-marketplace repository instead of quay.io."
}

variable "enable_firebase_community_builder_container_creation" {
  type        = bool
  description = "Enable Firebase Community Builder Container Creation"
  default     = true
}

variable "lms_enabled" {
  type        = bool
  description = "Flag to deploy the LMS / Classroom related services"
  default     = false
}

variable "matching_engine_enabled" {
  type        = bool
  description = "Flag to deploy Matching Engine"
  default     = false
}

variable "monitoring_enable_managed_prometheus" {
  type        = bool
  description = "Configuration for Managed Service for Prometheus. Whether or not the managed collection is enabled."
  default     = false
}

variable "monitoring_enabled_components" {
  type        = list(string)
  description = "List of services to monitor: SYSTEM_COMPONENTS, WORKLOADS (provider version >= 3.89.0). Empty list is default GKE configuration."
  default     = []
}

##########################################
# Start Content Serving Bucket variables #
##########################################

variable "content_serving_bucket_name" {
  description = "Content serving bucket name"
  type        = string
  default     = null
}

variable "content_serving_bucket_tag_value" {
  description = "The TagValue of the TagBinding in format tagValue/{name}. If it's null, tagBinding will be disabled."
  type        = string
  default     = null
}

variable "content_serving_bucket_additional_cors_origins" {
  type        = list(string)
  description = "Additional CORS origin filters required for content serving bucket"
  default     = []
}

##########################################
# End Content Serving Bucket variables #
##########################################

##########################################
# Variables for LRS Module - Start #
##########################################

variable "enable_lrs" {
  type        = bool
  description = "Flag to deploy LRS Module"
  default     = false
}

variable "lrs_dataset_id" {
  description = "Unique ID for the dataset being provisioned."
  type        = string
  default     = "lrs"
}

variable "lrs_dataset_name" {
  description = "Friendly name for the dataset being provisioned."
  type        = string
  default     = "lrs"
}

variable "lrs_description" {
  description = "Dataset description."
  type        = string
  default     = "Dataset to be used for LRS purposes"
}

variable "lrs_location" {
  description = "The regional location for the dataset only US and EU are allowed in module"
  type        = string
  default     = "US"
}

variable "lrs_delete_contents_on_destroy" {
  description = "(Optional) If set to true, delete all the tables in the dataset when destroying the resource; otherwise, destroying the resource will fail if tables are present."
  type        = bool
  default     = false
}

variable "lrs_deletion_protection" {
  description = "Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail"
  type        = bool
  default     = true
}

variable "lrs_dataset_labels" {
  description = "Key value pairs in a map for dataset labels"
  type        = map(string)
  default     = {}
}

variable "lrs_tables" {
  description = "A list of objects which include table_id, schema, clustering, time_partitioning, range_partitioning, expiration_time and labels."
  default     = []
  type = list(object({
    table_id   = string,
    schema     = string,
    clustering = list(string),
    time_partitioning = object({
      expiration_ms            = string,
      field                    = string,
      type                     = string,
      require_partition_filter = bool,
    }),
    range_partitioning = object({
      field = string,
      range = object({
        start    = string,
        end      = string,
        interval = string,
      }),
    }),
    expiration_time = string,
    labels          = map(string),
  }))
}

variable "lrs_views" {
  description = "A list of objects which include view_id and view query"
  default     = []
  type = list(object({
    view_id        = string,
    query          = string,
    use_legacy_sql = bool,
    labels         = map(string),
  }))
}

variable "lrs_external_tables" {
  description = "A list of objects which include table_id, expiration_time, external_data_configuration, and labels."
  default     = []
  type = list(object({
    table_id              = string,
    autodetect            = bool,
    compression           = string,
    ignore_unknown_values = bool,
    max_bad_records       = number,
    schema                = string,
    source_format         = string,
    source_uris           = list(string),
    csv_options = object({
      quote                 = string,
      allow_jagged_rows     = bool,
      allow_quoted_newlines = bool,
      encoding              = string,
      field_delimiter       = string,
      skip_leading_rows     = number,
    }),
    google_sheets_options = object({
      range             = string,
      skip_leading_rows = number,
    }),
    hive_partitioning_options = object({
      mode              = string,
      source_uri_prefix = string,
    }),
    expiration_time = string,
    labels          = map(string),
  }))
}
##########################################
# Variables for LRS Module - End #
##########################################

###############################
# Start Memorystore variables #
###############################
variable "enable_memorystore" {
  description = "If memorystore(redis) needs to be enabled."
  type        = bool
  default     = false
}

variable "memorystore_name" {
  description = "Memorystore Name."
  type        = string
  default     = "cloud-memorystore"
}

variable "memorystore_enable_apis" {
  description = "Enable the memorystore api."
  type        = bool
  default     = true
}

variable "memorystore_tier" {
  description = "Memorystore tier 'BASIC' or 'STANDARD_HA'."
  type        = string
  default     = "STANDARD_HA"
}

variable "memorystore_authorized_network" {
  description = "The full name of the Google Compute Engine network to which the instance is connected. If left unspecified, the default network will be used."
  type        = string
  default     = null
}

variable "memorystore_connect_mode" {
  description = "Memorystore Connection mode. DIRECT_PEERING or PRIVATE_SERVICE_ACCESS"
  type        = string
  default     = "DIRECT_PEERING"
}

variable "memorystore_reserved_ip_range" {
  description = "Default reserved IP range"
  type        = string
  default     = null
}

variable "memorystore_read_replicas_mode" {
  description = "Read replicas to be 'READ_REPLICAS_DISABLED', 'READ_REPLICAS_ENABLED'."
  type        = string
  default     = "READ_REPLICAS_DISABLED"
  validation {
    condition     = contains(["READ_REPLICAS_DISABLED", "READ_REPLICAS_ENABLED"], var.memorystore_read_replicas_mode)
    error_message = "Either READ_REPLICAS_DISABLED or READ_REPLICAS_ENABLED (This will required to set memorystore_replica_count variable > 0)"
  }
}

variable "memorystore_replica_count" {
  description = "Count of read replicas, if memorystore_read_replicas_mode is enabled."
  type        = number
  default     = null
}

variable "memorystore_memory_size_gb" {
  description = "Memory Size in GBs."
  type        = number
  default     = 1
}

variable "memorystore_redis_configs" {
  description = "Memorystore redis configuration."
  type        = map(any)
  default     = {}
}

variable "memorystore_transit_encryption_mode" {
  description = "Transit encryption mode."
  type        = string
  default     = "SERVER_AUTHENTICATION"
}
###############################
# End Memorystore variables #
###############################

variable "additional_nginx_cors_allow_origin" {
  type        = list(string)
  description = "Additional CORS origin filters required for nginx ingress module"
  default     = []
}

#######################################
# Start - Artifact Registry Variables #
#######################################

variable "create_artifact_registry_repository" {
  description = "Boolean Variable to enable(value = true)/disable(value = false) the creation of artifact registry"
  type        = bool
  default     = false
}

variable "artifact_registry_repository_location" {
  type        = string
  description = "Artifact Registry Location"
  default     = "us-central1"
}

variable "artifact_registry_repository_id" {
  type        = string
  description = "The name of the artifact registry"
  default     = "docker-repo"
}

variable "artifact_registry_repository_description" {
  type        = string
  description = "Description"
  default     = "Artifact Registry for storing Docker Images"
}

#######################################
# End - Artifact Registry Variables #
#######################################

variable "create_nginx_ingress" {
  type        = bool
  description = "Create NGINX Ingress"
  default     = true
}

#######################################
#        Start - LMS Variables        #
#######################################

variable "lms_bigquery_location" {
  type        = string
  description = "Biguqery location for LMS module"
  default     = "US"
}

#######################################
#        End - LMS Variables        #
#######################################

#######################################################
#        Start - Stackdriver Adapter Variables        #
#######################################################

variable "enable_stackdriver_adapter" {
  type        = bool
  description = "Enable Stackdriver Adapter module"
  default     = false
}

#######################################################
#         End - Stackdriver Adapter Variables         #
#######################################################

#######################################################
#  Start - Service Accounts Microservices Variables   #
#######################################################

variable "enable_service_accounts_microservices" {
  type        = bool
  description = "Enable Service Accounts Microservices module"
  default     = false
}

variable "gke_pod_microservices_common_roles" {
  type        = list(string)
  description = "Common roles utilized by each microservice's service account"
  default = [
    "roles/logging.logWriter",
  ]
}

variable "gke_pod_microservices_sa_iam_bindings" {
  description = " A list of objects, where each object represents a microservice's service account and its associated IAM bindings."
  type = list(object({
    sa_name          = string
    use_common_roles = bool
    additional_roles = list(string)
  }))
  default = []
}

#######################################################
#  End - Service Accounts Microservices Variables     #
#######################################################

##################################
#        Start - Firebase        #
##################################
variable "firebase_init" {
  type        = bool
  description = "Flag to deploy App Engine for firestore"
  default     = true
}
##################################
#        End - Firebase          #
##################################

#######################################################
#  Start - Logging & Alerting Modules                 #
#######################################################

variable "enable_logging_module" {
  description = "Boolean Variable to enable(value = true)/disable(value = false) the logging module"
  type        = bool
  default     = false
}

variable "logging_metric" {
  description = "A list of objects, where each object represents a log based metric and its details."
  type = list(object({
    name        = string
    description = optional(string)
    filter      = string
    metric_descriptor = optional(object({
      unit         = optional(string)
      value_type   = string
      metric_kind  = string
      display_name = optional(string)
    }))
    disabled = optional(bool)
  }))
  default = []
}

variable "enable_create_alerting" {
  type        = bool
  description = "Flag to enable Alerting Module to create Alert Policies & Notification Channel"
  default     = false
}

variable "alerting_notify_emails" {
  type        = map(string)
  description = "Notification Channel Emails"
  default     = {}
}

variable "alerting_document_path" {
  type        = string
  description = "Path to the Alert Policy with extention *.yaml or *.yml"
  default     = ""
}

#######################################################
#  End - Logging & Alerting Modules                   #
#######################################################

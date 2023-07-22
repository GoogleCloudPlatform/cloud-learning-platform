# TODO: pin versions of everything
# TODO: add taint to gke cluster

locals {
  web_app_domain  = var.web_app_domain != null ? "${var.web_app_domain}.${var.base_domain}" : "${var.project_id}.${var.base_domain}"
  ckt_app_domain  = var.ckt_app_domain != null ? "${var.ckt_app_domain}.${var.base_domain}" : "${var.project_id}-ckt.${var.base_domain}"
  api_domain      = var.api_domain != null ? "${var.api_domain}.${var.base_domain}" : "${var.project_id}-api.${var.base_domain}"
  gclb_api_domain = var.gclb_api_domain != null ? "${var.gclb_api_domain}.${var.base_domain}" : "${var.project_id}-gclb-api.${var.base_domain}"
}

module "project_services" {
  source     = "../project_services"
  project_id = var.project_id
}

module "vpc_network" {
  source = "../networking"
  count  = var.existing_custom_vpc ? 0 : 1

  vpc_network = var.vpc_network
  project_id  = var.project_id
  region      = var.region
  depends_on = [
    module.project_services
  ]
}

moved {
  from = module.vpc_network
  to   = module.vpc_network[0]
}

module "service_accounts" {
  source     = "../service_accounts"
  project_id = var.project_id

  depends_on = [
    module.project_services
  ]
}

module "service_accounts_microservices" {
  source                                = "../service_accounts_microservices"
  project_id                            = var.project_id
  gke_pod_microservices_sa_iam_bindings = var.enable_service_accounts_microservices ? var.gke_pod_microservices_sa_iam_bindings : []
  gke_pod_microservices_common_roles    = var.gke_pod_microservices_common_roles

  depends_on = [
    module.project_services
  ]
}

module "storage" {
  source         = "../storage"
  project_id     = var.project_id
  region         = var.bucket_region_or_multiregion
  web_app_domain = local.web_app_domain

  depends_on = [
    module.project_services
  ]
}

# wait for Firebase API to spin up
# TODO: test timer? may need more?
resource "time_sleep" "wait_30_seconds" {
  depends_on = [module.project_services]

  create_duration = "30s"
}

module "firebase" {
  source                     = "../firebase"
  project_id                 = var.project_id
  firestore_region           = var.firestore_region
  github_owner               = var.github_owner
  github_ref                 = var.github_ref
  api_domain                 = local.api_domain
  ai_tutor_whitelist_domains = var.ai_tutor_whitelist_domains
  ai_tutor_whitelist_emails  = var.ai_tutor_whitelist_emails
  ckt_whitelist_domains      = var.ckt_whitelist_domains
  ckt_whitelist_emails       = var.ckt_whitelist_emails
  firebase_init              = var.firebase_init

  depends_on = [
    module.project_services,
    time_sleep.wait_30_seconds
  ]
}

#TODO: rename
module "gke" {
  source                               = "../gke"
  project_id                           = var.project_id
  region                               = var.region
  release_channel                      = var.release_channel
  gpu_np_max_count                     = var.gpu_np_max_count
  gke_cluster_zones                    = var.gke_cluster_zones
  master_authorized_networks           = var.master_authorized_networks
  network                              = var.network
  subnetwork                           = var.subnetwork
  ip_range_pods                        = var.ip_range_pods
  ip_range_services                    = var.ip_range_services
  network_project_id                   = var.network_project_id != null ? var.network_project_id : var.project_id
  max_pods_per_node                    = var.max_pods_per_node
  datapath_provider                    = var.datapath_provider
  enable_vertical_pod_autoscaling      = var.enable_vertical_pod_autoscaling
  enable_shielded_nodes                = var.enable_shielded_nodes
  node_pools_create_before_destroy     = var.node_pools_create_before_destroy
  monitoring_enable_managed_prometheus = var.monitoring_enable_managed_prometheus
  gke_pod_sa_email                     = module.service_accounts.gke_pod_sa_email

  depends_on = [
    module.vpc_network,
    module.service_accounts
  ]
}

module "firebase_community_builder_container" {
  source                                               = "../firebase_community_builder_container"
  project_id                                           = var.project_id
  enable_firebase_community_builder_container_creation = var.enable_firebase_community_builder_container_creation
}

module "ingress" {
  source               = "../ingress"
  create_nginx_ingress = var.create_nginx_ingress
  cert_issuer_email    = var.cert_issuer_email
  api_domain           = local.api_domain
  web_app_domain       = local.web_app_domain
  ckt_app_domain       = local.ckt_app_domain

  enable_certman_gcr_io_images = var.enable_certman_gcr_io_images

  additional_nginx_cors_allow_origin = var.additional_nginx_cors_allow_origin

  depends_on = [
    module.gke,
  ]
}

module "ingress_gclb" {
  source = "../ingress_gclb"
  count  = var.lms_enabled ? 1 : 0

  cert_issuer_email = var.cert_issuer_email
  api_domain        = local.gclb_api_domain
  web_app_domain    = local.web_app_domain
  ckt_app_domain    = local.ckt_app_domain

  depends_on = [
    module.gke,
  ]
}

module "secrets" {
  source                                        = "../secrets"
  project_id                                    = var.project_id
  region                                        = var.region
  enable_secret_manager_secret_version_creation = var.enable_secret_manager_secret_version_creation
  enable_signurl_key_rotation                   = var.enable_signurl_key_rotation
  enable_service_account_key_creation           = var.enable_service_account_key_creation
  enable_kubernetes_secret_creation             = var.enable_kubernetes_secret_creation

  depends_on = [
    module.gke,
  ]
}

module "lms" {
  source = "../lms"
  count  = var.lms_enabled ? 1 : 0

  project_id = var.project_id
  region     = var.region

  firebase_project = module.firebase.firebase_project.project

  bigquery_location = var.lms_bigquery_location
}

module "matching_engine" {
  source = "../matching_engine"
  count  = var.matching_engine_enabled ? 1 : 0

  project_id = var.project_id
  region     = var.region
}

module "lrs" {
  source = "../lrs"
  count  = var.enable_lrs ? 1 : 0

  dataset_id                 = var.lrs_dataset_id
  dataset_name               = var.lrs_dataset_name
  description                = var.lrs_description
  location                   = var.lrs_location
  delete_contents_on_destroy = var.lrs_delete_contents_on_destroy
  deletion_protection        = var.lrs_deletion_protection
  project_id                 = var.project_id
  dataset_labels             = var.lrs_dataset_labels
  tables                     = var.lrs_tables
  views                      = var.lrs_views
  external_tables            = var.lrs_external_tables
}

# Used Module https://registry.terraform.io/modules/terraform-google-modules/memorystore/google/7.0.0
# Possible values for attributes can be found at https://cloud.google.com/memorystore/docs/redis/reference/rest/v1/projects.locations.instances#resource:-instance
module "memorystore" {
  source  = "terraform-google-modules/memorystore/google"
  version = "~> 7.0"

  count = var.enable_memorystore ? 1 : 0

  name         = var.memorystore_name
  project      = var.project_id
  display_name = var.memorystore_name
  region       = var.region

  tier        = var.memorystore_tier
  enable_apis = var.memorystore_enable_apis

  authorized_network = var.memorystore_authorized_network
  connect_mode       = var.memorystore_connect_mode
  reserved_ip_range  = var.memorystore_reserved_ip_range

  read_replicas_mode      = var.memorystore_read_replicas_mode
  replica_count           = var.memorystore_replica_count
  memory_size_gb          = var.memorystore_memory_size_gb
  redis_configs           = var.memorystore_redis_configs
  transit_encryption_mode = var.memorystore_transit_encryption_mode
}

module "logging" {
  source         = "../logging"
  count          = var.enable_logging_module ? 1 : 0
  logging_metric = var.logging_metric
  project_id     = var.project_id
}

module "create_alerting" {
  source              = "./../alerting"
  project_id          = var.project_id
  count               = var.enable_create_alerting ? 1 : 0
  alert_notify_emails = var.alerting_notify_emails
  document_path       = var.alerting_document_path
}

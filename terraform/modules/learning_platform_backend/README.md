<!-- BEGIN_TF_DOCS -->

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_google"></a> [google](#requirement\_google) | > 4.50.0 |
| <a name="requirement_helm"></a> [helm](#requirement\_helm) | >= 2.7.0 |
| <a name="requirement_kubectl"></a> [kubectl](#requirement\_kubectl) | >= 1.14.0 |
## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | > 4.50.0 |
| <a name="provider_time"></a> [time](#provider\_time) | n/a |
## Resources

| Name | Type |
|------|------|
| [google_artifact_registry_repository.default](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/artifact_registry_repository) | resource |
| [google_storage_bucket.content_serving_bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket) | resource |
| [google_storage_bucket_iam_binding.content_serving_bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_iam_binding) | resource |
| [google_tags_tag_binding.content_serving_bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/tags_tag_binding) | resource |
| [time_sleep.wait_30_seconds](https://registry.terraform.io/providers/hashicorp/time/latest/docs/resources/sleep) | resource |
| [google_client_config.default](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/client_config) | data source |
## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_create_alerting"></a> [create\_alerting](#module\_create\_alerting) | ./../alerting | n/a |
| <a name="module_firebase"></a> [firebase](#module\_firebase) | ../firebase | n/a |
| <a name="module_firebase_community_builder_container"></a> [firebase\_community\_builder\_container](#module\_firebase\_community\_builder\_container) | ../firebase_community_builder_container | n/a |
| <a name="module_gke"></a> [gke](#module\_gke) | ../gke | n/a |
| <a name="module_ingress"></a> [ingress](#module\_ingress) | ../ingress | n/a |
| <a name="module_ingress_gclb"></a> [ingress\_gclb](#module\_ingress\_gclb) | ../ingress_gclb | n/a |
| <a name="module_lms"></a> [lms](#module\_lms) | ../lms | n/a |
| <a name="module_logging"></a> [logging](#module\_logging) | ../logging | n/a |
| <a name="module_lrs"></a> [lrs](#module\_lrs) | ../lrs | n/a |
| <a name="module_matching_engine"></a> [matching\_engine](#module\_matching\_engine) | ../matching_engine | n/a |
| <a name="module_memorystore"></a> [memorystore](#module\_memorystore) | terraform-google-modules/memorystore/google | ~> 7.0 |
| <a name="module_project_services"></a> [project\_services](#module\_project\_services) | ../project_services | n/a |
| <a name="module_secrets"></a> [secrets](#module\_secrets) | ../secrets | n/a |
| <a name="module_service_accounts"></a> [service\_accounts](#module\_service\_accounts) | ../service_accounts | n/a |
| <a name="module_service_accounts_microservices"></a> [service\_accounts\_microservices](#module\_service\_accounts\_microservices) | ../service_accounts_microservices | n/a |
| <a name="module_stackdriver_adapter"></a> [stackdriver\_adapter](#module\_stackdriver\_adapter) | ../stackdriver_adapter | n/a |
| <a name="module_storage"></a> [storage](#module\_storage) | ../storage | n/a |
| <a name="module_vpc_network"></a> [vpc\_network](#module\_vpc\_network) | ../networking | n/a |
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_additional_nginx_cors_allow_origin"></a> [additional\_nginx\_cors\_allow\_origin](#input\_additional\_nginx\_cors\_allow\_origin) | Additional CORS origin filters required for nginx ingress module | `list(string)` | `[]` | no |
| <a name="input_ai_tutor_whitelist_domains"></a> [ai\_tutor\_whitelist\_domains](#input\_ai\_tutor\_whitelist\_domains) | Comma separated list of email domains that should have access to AI Tutor | `string` | n/a | yes |
| <a name="input_ai_tutor_whitelist_emails"></a> [ai\_tutor\_whitelist\_emails](#input\_ai\_tutor\_whitelist\_emails) | Comma separated list of individual emails that should have access to AI Tutor | `string` | n/a | yes |
| <a name="input_alerting_document_path"></a> [alerting\_document\_path](#input\_alerting\_document\_path) | Path to the Alert Policy with extention *.yaml or *.yml | `string` | `""` | no |
| <a name="input_alerting_notify_emails"></a> [alerting\_notify\_emails](#input\_alerting\_notify\_emails) | Notification Channel Emails | `map(string)` | `{}` | no |
| <a name="input_api_domain"></a> [api\_domain](#input\_api\_domain) | Subdomain name for backend | `string` | `null` | no |
| <a name="input_artifact_registry_repository_description"></a> [artifact\_registry\_repository\_description](#input\_artifact\_registry\_repository\_description) | Description | `string` | `"Artifact Registry for storing Docker Images"` | no |
| <a name="input_artifact_registry_repository_id"></a> [artifact\_registry\_repository\_id](#input\_artifact\_registry\_repository\_id) | The name of the artifact registry | `string` | `"docker-repo"` | no |
| <a name="input_artifact_registry_repository_location"></a> [artifact\_registry\_repository\_location](#input\_artifact\_registry\_repository\_location) | Artifact Registry Location | `string` | `"us-central1"` | no |
| <a name="input_base_domain"></a> [base\_domain](#input\_base\_domain) | base domain or subdomain for firebase and APIs | `string` | n/a | yes |
| <a name="input_bucket_region_or_multiregion"></a> [bucket\_region\_or\_multiregion](#input\_bucket\_region\_or\_multiregion) | GCP Region or Multiregion | `string` | n/a | yes |
| <a name="input_cert_issuer_email"></a> [cert\_issuer\_email](#input\_cert\_issuer\_email) | email of the cert issuer | `string` | n/a | yes |
| <a name="input_ckt_app_domain"></a> [ckt\_app\_domain](#input\_ckt\_app\_domain) | Subdomain name for frontend of CKT application | `string` | `null` | no |
| <a name="input_ckt_whitelist_domains"></a> [ckt\_whitelist\_domains](#input\_ckt\_whitelist\_domains) | Comma separated list of email domains that should have access to CKT | `string` | n/a | yes |
| <a name="input_ckt_whitelist_emails"></a> [ckt\_whitelist\_emails](#input\_ckt\_whitelist\_emails) | Comma separated list of individual emails that should have access to CKT | `string` | n/a | yes |
| <a name="input_content_serving_bucket_additional_cors_origins"></a> [content\_serving\_bucket\_additional\_cors\_origins](#input\_content\_serving\_bucket\_additional\_cors\_origins) | Additional CORS origin filters required for content serving bucket | `list(string)` | `[]` | no |
| <a name="input_content_serving_bucket_name"></a> [content\_serving\_bucket\_name](#input\_content\_serving\_bucket\_name) | Content serving bucket name | `string` | `null` | no |
| <a name="input_content_serving_bucket_tag_value"></a> [content\_serving\_bucket\_tag\_value](#input\_content\_serving\_bucket\_tag\_value) | The TagValue of the TagBinding in format tagValue/{name}. If it's null, tagBinding will be disabled. | `string` | `null` | no |
| <a name="input_create_artifact_registry_repository"></a> [create\_artifact\_registry\_repository](#input\_create\_artifact\_registry\_repository) | Boolean Variable to enable(value = true)/disable(value = false) the creation of artifact registry | `bool` | `false` | no |
| <a name="input_create_nginx_ingress"></a> [create\_nginx\_ingress](#input\_create\_nginx\_ingress) | Create NGINX Ingress | `bool` | `true` | no |
| <a name="input_datapath_provider"></a> [datapath\_provider](#input\_datapath\_provider) | The desired datapath provider for this cluster. By default, DATAPATH\_PROVIDER\_UNSPECIFIED enables the IPTables-based kube-proxy implementation. ADVANCED\_DATAPATH enables Dataplane-V2 feature. | `string` | `"ADVANCED_DATAPATH"` | no |
| <a name="input_enable_certman_gcr_io_images"></a> [enable\_certman\_gcr\_io\_images](#input\_enable\_certman\_gcr\_io\_images) | Enabling this to use cert-manager images from the gcr.io/google-marketplace repository instead of quay.io. | `bool` | `false` | no |
| <a name="input_enable_create_alerting"></a> [enable\_create\_alerting](#input\_enable\_create\_alerting) | Flag to enable Alerting Module to create Alert Policies & Notification Channel | `bool` | `false` | no |
| <a name="input_enable_firebase_community_builder_container_creation"></a> [enable\_firebase\_community\_builder\_container\_creation](#input\_enable\_firebase\_community\_builder\_container\_creation) | Enable Firebase Community Builder Container Creation | `bool` | `true` | no |
| <a name="input_enable_kubernetes_secret_creation"></a> [enable\_kubernetes\_secret\_creation](#input\_enable\_kubernetes\_secret\_creation) | Enable Kubernetes Secret Creation | `bool` | `true` | no |
| <a name="input_enable_logging_module"></a> [enable\_logging\_module](#input\_enable\_logging\_module) | Boolean Variable to enable(value = true)/disable(value = false) the logging module | `bool` | `false` | no |
| <a name="input_enable_lrs"></a> [enable\_lrs](#input\_enable\_lrs) | Flag to deploy LRS Module | `bool` | `false` | no |
| <a name="input_enable_memorystore"></a> [enable\_memorystore](#input\_enable\_memorystore) | If memorystore(redis) needs to be enabled. | `bool` | `false` | no |
| <a name="input_enable_secret_manager_secret_version_creation"></a> [enable\_secret\_manager\_secret\_version\_creation](#input\_enable\_secret\_manager\_secret\_version\_creation) | Enable Secret Manager Secret Version Creation | `bool` | `true` | no |
| <a name="input_enable_service_account_key_creation"></a> [enable\_service\_account\_key\_creation](#input\_enable\_service\_account\_key\_creation) | Enable Service Account Key Creation | `bool` | `true` | no |
| <a name="input_enable_service_accounts_microservices"></a> [enable\_service\_accounts\_microservices](#input\_enable\_service\_accounts\_microservices) | Enable Service Accounts Microservices module | `bool` | `false` | no |
| <a name="input_enable_shielded_nodes"></a> [enable\_shielded\_nodes](#input\_enable\_shielded\_nodes) | Enable Shielded Nodes features on all nodes in this cluster | `bool` | `true` | no |
| <a name="input_enable_signurl_key_rotation"></a> [enable\_signurl\_key\_rotation](#input\_enable\_signurl\_key\_rotation) | Enable SignURL Key Rotation | `bool` | `true` | no |
| <a name="input_enable_stackdriver_adapter"></a> [enable\_stackdriver\_adapter](#input\_enable\_stackdriver\_adapter) | Enable Stackdriver Adapter module | `bool` | `false` | no |
| <a name="input_enable_vertical_pod_autoscaling"></a> [enable\_vertical\_pod\_autoscaling](#input\_enable\_vertical\_pod\_autoscaling) | Vertical Pod Autoscaling automatically adjusts the resources of pods controlled by it | `bool` | `true` | no |
| <a name="input_env"></a> [env](#input\_env) | specify the Cloud environment | `string` | `"dev"` | no |
| <a name="input_existing_custom_vpc"></a> [existing\_custom\_vpc](#input\_existing\_custom\_vpc) | custom vpc created by the clients/users(manually) True/False | `bool` | `false` | no |
| <a name="input_firebase_init"></a> [firebase\_init](#input\_firebase\_init) | Flag to deploy App Engine for firestore | `bool` | `true` | no |
| <a name="input_firestore_region"></a> [firestore\_region](#input\_firestore\_region) | Firestore Region - must be app\_engine region | `string` | n/a | yes |
| <a name="input_gclb_api_domain"></a> [gclb\_api\_domain](#input\_gclb\_api\_domain) | Subdomain name for backend, GCLB version | `string` | `null` | no |
| <a name="input_github_owner"></a> [github\_owner](#input\_github\_owner) | Your github username (or github org if enterprise deployment) | `string` | `"GPS-Solutions"` | no |
| <a name="input_github_ref"></a> [github\_ref](#input\_github\_ref) | Github ref to use for cloud build triggers | `string` | `"refs/tags/v2.0.0-beta12.7-demo"` | no |
| <a name="input_gke_cluster_zones"></a> [gke\_cluster\_zones](#input\_gke\_cluster\_zones) | specify the zones for the cluster region | `list(string)` | n/a | yes |
| <a name="input_gke_pod_microservices_common_roles"></a> [gke\_pod\_microservices\_common\_roles](#input\_gke\_pod\_microservices\_common\_roles) | Common roles utilized by each microservice's service account | `list(string)` | <pre>[<br>  "roles/logging.logWriter"<br>]</pre> | no |
| <a name="input_gke_pod_microservices_sa_iam_bindings"></a> [gke\_pod\_microservices\_sa\_iam\_bindings](#input\_gke\_pod\_microservices\_sa\_iam\_bindings) | A list of objects, where each object represents a microservice's service account and its associated IAM bindings. | <pre>list(object({<br>    sa_name          = string<br>    use_common_roles = bool<br>    additional_roles = list(string)<br>  }))</pre> | `[]` | no |
| <a name="input_gpu_np_max_count"></a> [gpu\_np\_max\_count](#input\_gpu\_np\_max\_count) | Max node pool count for auto scaling (0 to disable GPU nodes) | `string` | `"6"` | no |
| <a name="input_ip_range_pods"></a> [ip\_range\_pods](#input\_ip\_range\_pods) | The name of the secondary subnet ip range to use for pods | `string` | `"secondary-pod-range-01"` | no |
| <a name="input_ip_range_services"></a> [ip\_range\_services](#input\_ip\_range\_services) | The name of the secondary subnet range to use for services | `string` | `"secondary-service-range-01"` | no |
| <a name="input_lms_bigquery_location"></a> [lms\_bigquery\_location](#input\_lms\_bigquery\_location) | Biguqery location for LMS module | `string` | `"US"` | no |
| <a name="input_lms_enabled"></a> [lms\_enabled](#input\_lms\_enabled) | Flag to deploy the LMS / Classroom related services | `bool` | `false` | no |
| <a name="input_logging_metric"></a> [logging\_metric](#input\_logging\_metric) | A list of objects, where each object represents a log based metric and its details. | <pre>list(object({<br>    name        = string<br>    description = optional(string)<br>    filter      = string<br>    metric_descriptor = optional(object({<br>      unit         = optional(string)<br>      value_type   = string<br>      metric_kind  = string<br>      display_name = optional(string)<br>    }))<br>    disabled = optional(bool)<br>  }))</pre> | `[]` | no |
| <a name="input_lrs_dataset_id"></a> [lrs\_dataset\_id](#input\_lrs\_dataset\_id) | Unique ID for the dataset being provisioned. | `string` | `"lrs"` | no |
| <a name="input_lrs_dataset_labels"></a> [lrs\_dataset\_labels](#input\_lrs\_dataset\_labels) | Key value pairs in a map for dataset labels | `map(string)` | `{}` | no |
| <a name="input_lrs_dataset_name"></a> [lrs\_dataset\_name](#input\_lrs\_dataset\_name) | Friendly name for the dataset being provisioned. | `string` | `"lrs"` | no |
| <a name="input_lrs_delete_contents_on_destroy"></a> [lrs\_delete\_contents\_on\_destroy](#input\_lrs\_delete\_contents\_on\_destroy) | (Optional) If set to true, delete all the tables in the dataset when destroying the resource; otherwise, destroying the resource will fail if tables are present. | `bool` | `false` | no |
| <a name="input_lrs_deletion_protection"></a> [lrs\_deletion\_protection](#input\_lrs\_deletion\_protection) | Whether or not to allow Terraform to destroy the instance. Unless this field is set to false in Terraform state, a terraform destroy or terraform apply that would delete the instance will fail | `bool` | `true` | no |
| <a name="input_lrs_description"></a> [lrs\_description](#input\_lrs\_description) | Dataset description. | `string` | `"Dataset to be used for LRS purposes"` | no |
| <a name="input_lrs_external_tables"></a> [lrs\_external\_tables](#input\_lrs\_external\_tables) | A list of objects which include table\_id, expiration\_time, external\_data\_configuration, and labels. | <pre>list(object({<br>    table_id              = string,<br>    autodetect            = bool,<br>    compression           = string,<br>    ignore_unknown_values = bool,<br>    max_bad_records       = number,<br>    schema                = string,<br>    source_format         = string,<br>    source_uris           = list(string),<br>    csv_options = object({<br>      quote                 = string,<br>      allow_jagged_rows     = bool,<br>      allow_quoted_newlines = bool,<br>      encoding              = string,<br>      field_delimiter       = string,<br>      skip_leading_rows     = number,<br>    }),<br>    google_sheets_options = object({<br>      range             = string,<br>      skip_leading_rows = number,<br>    }),<br>    hive_partitioning_options = object({<br>      mode              = string,<br>      source_uri_prefix = string,<br>    }),<br>    expiration_time = string,<br>    labels          = map(string),<br>  }))</pre> | `[]` | no |
| <a name="input_lrs_location"></a> [lrs\_location](#input\_lrs\_location) | The regional location for the dataset only US and EU are allowed in module | `string` | `"US"` | no |
| <a name="input_lrs_tables"></a> [lrs\_tables](#input\_lrs\_tables) | A list of objects which include table\_id, schema, clustering, time\_partitioning, range\_partitioning, expiration\_time and labels. | <pre>list(object({<br>    table_id   = string,<br>    schema     = string,<br>    clustering = list(string),<br>    time_partitioning = object({<br>      expiration_ms            = string,<br>      field                    = string,<br>      type                     = string,<br>      require_partition_filter = bool,<br>    }),<br>    range_partitioning = object({<br>      field = string,<br>      range = object({<br>        start    = string,<br>        end      = string,<br>        interval = string,<br>      }),<br>    }),<br>    expiration_time = string,<br>    labels          = map(string),<br>  }))</pre> | `[]` | no |
| <a name="input_lrs_views"></a> [lrs\_views](#input\_lrs\_views) | A list of objects which include view\_id and view query | <pre>list(object({<br>    view_id        = string,<br>    query          = string,<br>    use_legacy_sql = bool,<br>    labels         = map(string),<br>  }))</pre> | `[]` | no |
| <a name="input_master_authorized_networks"></a> [master\_authorized\_networks](#input\_master\_authorized\_networks) | List of master authorized networks. If none are provided, disallow external access (except the cluster node IPs, which GKE automatically whitelists). | `list(object({ cidr_block = string, display_name = string }))` | <pre>[<br>  {<br>    "cidr_block": "0.0.0.0/0",<br>    "display_name": "all-IPs"<br>  }<br>]</pre> | no |
| <a name="input_matching_engine_enabled"></a> [matching\_engine\_enabled](#input\_matching\_engine\_enabled) | Flag to deploy Matching Engine | `bool` | `false` | no |
| <a name="input_max_pods_per_node"></a> [max\_pods\_per\_node](#input\_max\_pods\_per\_node) | Maximun pods to be assigned to the nodes | `string` | `"110"` | no |
| <a name="input_memorystore_authorized_network"></a> [memorystore\_authorized\_network](#input\_memorystore\_authorized\_network) | The full name of the Google Compute Engine network to which the instance is connected. If left unspecified, the default network will be used. | `string` | `null` | no |
| <a name="input_memorystore_connect_mode"></a> [memorystore\_connect\_mode](#input\_memorystore\_connect\_mode) | Memorystore Connection mode. DIRECT\_PEERING or PRIVATE\_SERVICE\_ACCESS | `string` | `"DIRECT_PEERING"` | no |
| <a name="input_memorystore_enable_apis"></a> [memorystore\_enable\_apis](#input\_memorystore\_enable\_apis) | Enable the memorystore api. | `bool` | `true` | no |
| <a name="input_memorystore_memory_size_gb"></a> [memorystore\_memory\_size\_gb](#input\_memorystore\_memory\_size\_gb) | Memory Size in GBs. | `number` | `1` | no |
| <a name="input_memorystore_name"></a> [memorystore\_name](#input\_memorystore\_name) | Memorystore Name. | `string` | `"cloud-memorystore"` | no |
| <a name="input_memorystore_read_replicas_mode"></a> [memorystore\_read\_replicas\_mode](#input\_memorystore\_read\_replicas\_mode) | Read replicas to be 'READ\_REPLICAS\_DISABLED', 'READ\_REPLICAS\_ENABLED'. | `string` | `"READ_REPLICAS_DISABLED"` | no |
| <a name="input_memorystore_redis_configs"></a> [memorystore\_redis\_configs](#input\_memorystore\_redis\_configs) | Memorystore redis configuration. | `map(any)` | `{}` | no |
| <a name="input_memorystore_replica_count"></a> [memorystore\_replica\_count](#input\_memorystore\_replica\_count) | Count of read replicas, if memorystore\_read\_replicas\_mode is enabled. | `number` | `null` | no |
| <a name="input_memorystore_reserved_ip_range"></a> [memorystore\_reserved\_ip\_range](#input\_memorystore\_reserved\_ip\_range) | Default reserved IP range | `string` | `null` | no |
| <a name="input_memorystore_tier"></a> [memorystore\_tier](#input\_memorystore\_tier) | Memorystore tier 'BASIC' or 'STANDARD\_HA'. | `string` | `"STANDARD_HA"` | no |
| <a name="input_memorystore_transit_encryption_mode"></a> [memorystore\_transit\_encryption\_mode](#input\_memorystore\_transit\_encryption\_mode) | Transit encryption mode. | `string` | `"SERVER_AUTHENTICATION"` | no |
| <a name="input_monitoring_enable_managed_prometheus"></a> [monitoring\_enable\_managed\_prometheus](#input\_monitoring\_enable\_managed\_prometheus) | Configuration for Managed Service for Prometheus. Whether or not the managed collection is enabled. | `bool` | `false` | no |
| <a name="input_monitoring_enabled_components"></a> [monitoring\_enabled\_components](#input\_monitoring\_enabled\_components) | List of services to monitor: SYSTEM\_COMPONENTS, WORKLOADS (provider version >= 3.89.0). Empty list is default GKE configuration. | `list(string)` | `[]` | no |
| <a name="input_multiregion"></a> [multiregion](#input\_multiregion) | multiregion location | `string` | `"us"` | no |
| <a name="input_network"></a> [network](#input\_network) | VPC network to host the gke cluster | `string` | `"vpc-01"` | no |
| <a name="input_network_project_id"></a> [network\_project\_id](#input\_network\_project\_id) | The project ID of the shared VPC's host (for shared vpc support) | `string` | `null` | no |
| <a name="input_node_pools_create_before_destroy"></a> [node\_pools\_create\_before\_destroy](#input\_node\_pools\_create\_before\_destroy) | Enable Shielded Nodes features on all nodes in this cluster | `bool` | `true` | no |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | GCP Project ID | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | GCP Region | `string` | n/a | yes |
| <a name="input_release_channel"></a> [release\_channel](#input\_release\_channel) | The release channel of this cluster. Accepted values are UNSPECIFIED, RAPID, REGULAR and STABLE. Defaults to UNSPECIFIED. | `string` | `"REGULAR"` | no |
| <a name="input_subnetwork"></a> [subnetwork](#input\_subnetwork) | VPC subnetwork which will be used by the cluster | `string` | `"vpc-01-subnet-01"` | no |
| <a name="input_vpc_network"></a> [vpc\_network](#input\_vpc\_network) | specify the vpc name | `string` | `"vpc-01"` | no |
| <a name="input_web_app_domain"></a> [web\_app\_domain](#input\_web\_app\_domain) | Subdomain name for frontend of Aitutor application | `string` | `null` | no |
## Outputs

| Name | Description |
|------|-------------|
| <a name="output_ai_tutor_firebase_api_key"></a> [ai\_tutor\_firebase\_api\_key](#output\_ai\_tutor\_firebase\_api\_key) | n/a |
| <a name="output_api_domain"></a> [api\_domain](#output\_api\_domain) | n/a |
| <a name="output_api_gclb_domain"></a> [api\_gclb\_domain](#output\_api\_gclb\_domain) | n/a |
| <a name="output_ca_certificate"></a> [ca\_certificate](#output\_ca\_certificate) | n/a |
| <a name="output_ckt_app_domain"></a> [ckt\_app\_domain](#output\_ckt\_app\_domain) | n/a |
| <a name="output_gke_cluster"></a> [gke\_cluster](#output\_gke\_cluster) | n/a |
| <a name="output_gke_cluster_id"></a> [gke\_cluster\_id](#output\_gke\_cluster\_id) | Adding try() to wrap those dependant variables below as a workaround to bypass the cyclic dependencies on cluster creation and providers. This approach remove the need to comment providers out first then uncomment later. See the usage of these vars in demo\_environment/providers.tf. |
| <a name="output_gke_endpoint"></a> [gke\_endpoint](#output\_gke\_endpoint) | n/a |
| <a name="output_ingress_gclb_ip_address"></a> [ingress\_gclb\_ip\_address](#output\_ingress\_gclb\_ip\_address) | n/a |
| <a name="output_ingress_ip_address"></a> [ingress\_ip\_address](#output\_ingress\_ip\_address) | n/a |
| <a name="output_lms_firebase_web_app_api_key"></a> [lms\_firebase\_web\_app\_api\_key](#output\_lms\_firebase\_web\_app\_api\_key) | n/a |
| <a name="output_lms_firebase_web_app_id"></a> [lms\_firebase\_web\_app\_id](#output\_lms\_firebase\_web\_app\_id) | n/a |
| <a name="output_web_app_domain"></a> [web\_app\_domain](#output\_web\_app\_domain) | n/a |

<!-- END_TF_DOCS -->
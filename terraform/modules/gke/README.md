<!-- BEGIN_TF_DOCS -->

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_google"></a> [google](#requirement\_google) | > 4.50.0 |
| <a name="requirement_kubectl"></a> [kubectl](#requirement\_kubectl) | >= 1.14.0 |
## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | > 4.50.0 |
| <a name="provider_kubectl"></a> [kubectl](#provider\_kubectl) | >= 1.14.0 |
| <a name="provider_kubernetes"></a> [kubernetes](#provider\_kubernetes) | n/a |
## Resources

| Name | Type |
|------|------|
| [google_service_account_iam_member.gsa-ksa-binding](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/service_account_iam_member) | resource |
| [kubectl_manifest.nvidia_driver_installer](https://registry.terraform.io/providers/gavinbunney/kubectl/latest/docs/resources/manifest) | resource |
| [kubernetes_service_account.ksa](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/service_account) | resource |
| [google_client_config.default](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/client_config) | data source |
## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_gke"></a> [gke](#module\_gke) | terraform-google-modules/kubernetes-engine/google//modules/beta-private-cluster-update-variant | 23.3.0 |
| <a name="module_service_accounts"></a> [service\_accounts](#module\_service\_accounts) | terraform-google-modules/service-accounts/google | ~> 4.1 |
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_datapath_provider"></a> [datapath\_provider](#input\_datapath\_provider) | The desired datapath provider for this cluster. By default, DATAPATH\_PROVIDER\_UNSPECIFIED enables the IPTables-based kube-proxy implementation. ADVANCED\_DATAPATH enables Dataplane-V2 feature. | `string` | n/a | yes |
| <a name="input_enable_shielded_nodes"></a> [enable\_shielded\_nodes](#input\_enable\_shielded\_nodes) | Enable Shielded Nodes features on all nodes in this cluster | `bool` | n/a | yes |
| <a name="input_enable_vertical_pod_autoscaling"></a> [enable\_vertical\_pod\_autoscaling](#input\_enable\_vertical\_pod\_autoscaling) | Vertical Pod Autoscaling automatically adjusts the resources of pods controlled by it | `bool` | n/a | yes |
| <a name="input_gke_cluster_zones"></a> [gke\_cluster\_zones](#input\_gke\_cluster\_zones) | specify the zones for the cluster region | `list(string)` | n/a | yes |
| <a name="input_gke_pod_sa_email"></a> [gke\_pod\_sa\_email](#input\_gke\_pod\_sa\_email) | the email of the main pod SA | `string` | n/a | yes |
| <a name="input_gpu_np_max_count"></a> [gpu\_np\_max\_count](#input\_gpu\_np\_max\_count) | Node pool max count for auto scaling (0 to disable GPU nodes) | `string` | n/a | yes |
| <a name="input_ip_range_pods"></a> [ip\_range\_pods](#input\_ip\_range\_pods) | The name of the secondary subnet ip range to use for pods | `string` | `"secondary-pod-range-01"` | no |
| <a name="input_ip_range_services"></a> [ip\_range\_services](#input\_ip\_range\_services) | The name of the secondary subnet range to use for services | `string` | `"secondary-service-range-01"` | no |
| <a name="input_master_authorized_networks"></a> [master\_authorized\_networks](#input\_master\_authorized\_networks) | List of master authorized networks. If none are provided, disallow external access (except the cluster node IPs, which GKE automatically whitelists). | `list(object({ cidr_block = string, display_name = string }))` | n/a | yes |
| <a name="input_max_pods_per_node"></a> [max\_pods\_per\_node](#input\_max\_pods\_per\_node) | Maximum pods to be assigned to the nodes | `string` | n/a | yes |
| <a name="input_monitoring_enable_managed_prometheus"></a> [monitoring\_enable\_managed\_prometheus](#input\_monitoring\_enable\_managed\_prometheus) | Configuration for Managed Service for Prometheus. Whether or not the managed collection is enabled. | `bool` | `false` | no |
| <a name="input_monitoring_enabled_components"></a> [monitoring\_enabled\_components](#input\_monitoring\_enabled\_components) | List of services to monitor: SYSTEM\_COMPONENTS, WORKLOADS (provider version >= 3.89.0). Empty list is default GKE configuration. | `list(string)` | `[]` | no |
| <a name="input_network"></a> [network](#input\_network) | VPC network to host the gke cluster | `string` | `"vpc-01"` | no |
| <a name="input_network_project_id"></a> [network\_project\_id](#input\_network\_project\_id) | The project ID of the shared VPC's host (for shared vpc support) | `string` | n/a | yes |
| <a name="input_node_pools_create_before_destroy"></a> [node\_pools\_create\_before\_destroy](#input\_node\_pools\_create\_before\_destroy) | TODO: copy paste from upstream module | `bool` | `true` | no |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | project ID | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | cluster region | `string` | n/a | yes |
| <a name="input_release_channel"></a> [release\_channel](#input\_release\_channel) | The release channel of this cluster. Accepted values are UNSPECIFIED, RAPID, REGULAR and STABLE. Defaults to UNSPECIFIED. | `string` | n/a | yes |
| <a name="input_subnetwork"></a> [subnetwork](#input\_subnetwork) | VPC subnetwork which will be used by the cluster | `string` | `"vpc-01-subnet-01"` | no |
## Outputs

| Name | Description |
|------|-------------|
| <a name="output_ca_certificate"></a> [ca\_certificate](#output\_ca\_certificate) | n/a |
| <a name="output_endpoint"></a> [endpoint](#output\_endpoint) | n/a |
| <a name="output_gke_cluster"></a> [gke\_cluster](#output\_gke\_cluster) | n/a |
| <a name="output_gke_cluster_id"></a> [gke\_cluster\_id](#output\_gke\_cluster\_id) | Adding try() to wrap those dependant variables below as a workaround to bypass the cyclic dependencies on cluster creation and providers. This approach removes the need to comment providers out first then uncomment later. |

<!-- END_TF_DOCS -->
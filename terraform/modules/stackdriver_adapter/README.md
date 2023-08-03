<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3.6 |
| <a name="requirement_google"></a> [google](#requirement\_google) | ~> 4.0, != 4.49.0, != 4.50.0 |
| <a name="requirement_helm"></a> [helm](#requirement\_helm) | >= 2.5.1 |
| <a name="requirement_kubectl"></a> [kubectl](#requirement\_kubectl) | >= 1.14.0 |
## Resources

| Name | Type |
|------|------|
| [google_service_account_iam_member.custom_metrics_sd_adapter](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/service_account_iam_member) | resource |
| [kubernetes_api_service_v1.apiservice_v1beta1_custom_metrics_k8s_io](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/api_service_v1) | resource |
| [kubernetes_api_service_v1.apiservice_v1beta1_external_metrics_k8s_io](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/api_service_v1) | resource |
| [kubernetes_api_service_v1.apiservice_v1beta2_custom_metrics_k8s_io](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/api_service_v1) | resource |
| [kubernetes_cluster_role_binding_v1.clusterrolebinding_custom_metrics_resource_reader](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/cluster_role_binding_v1) | resource |
| [kubernetes_cluster_role_binding_v1.clusterrolebinding_custom_metrics_system_auth_delegator](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/cluster_role_binding_v1) | resource |
| [kubernetes_cluster_role_binding_v1.clusterrolebinding_external_metrics_reader](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/cluster_role_binding_v1) | resource |
| [kubernetes_cluster_role_v1.clusterrole_custom_metrics_resource_reader](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/cluster_role_v1) | resource |
| [kubernetes_cluster_role_v1.clusterrole_external_metrics_reader](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/cluster_role_v1) | resource |
| [kubernetes_deployment_v1.deployment_custom_metrics_custom_metrics_stackdriver_adapter](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/deployment_v1) | resource |
| [kubernetes_namespace_v1.namespace_custom_metrics](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/namespace_v1) | resource |
| [kubernetes_role_binding_v1.rolebinding_kube_system_custom_metrics_auth_reader](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/role_binding_v1) | resource |
| [kubernetes_service_account_v1.custom_metrics_stackdriver_adapter](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/service_account_v1) | resource |
| [kubernetes_service_v1.service_custom_metrics_custom_metrics_stackdriver_adapter](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/service_v1) | resource |
## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_custom_metrics_sd_adapter_sa"></a> [custom\_metrics\_sd\_adapter\_sa](#module\_custom\_metrics\_sd\_adapter\_sa) | terraform-google-modules/service-accounts/google | ~> 3.0 |
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | GCP Project ID | `string` | n/a | yes |
## Outputs

No outputs.
<!-- END_TF_DOCS -->
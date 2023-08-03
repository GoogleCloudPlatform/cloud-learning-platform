<!-- BEGIN_TF_DOCS -->

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_gke_pod_microservices_sa_iam_bindings"></a> [gke\_pod\_microservices\_sa\_iam\_bindings](#module\_gke\_pod\_microservices\_sa\_iam\_bindings) | terraform-google-modules/service-accounts/google | ~> 4.1 |
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_gke_pod_microservices_common_roles"></a> [gke\_pod\_microservices\_common\_roles](#input\_gke\_pod\_microservices\_common\_roles) | Common roles utilized by each microservice's service account | `list` | `[]` | no |
| <a name="input_gke_pod_microservices_sa_iam_bindings"></a> [gke\_pod\_microservices\_sa\_iam\_bindings](#input\_gke\_pod\_microservices\_sa\_iam\_bindings) | A list of objects, where each object represents a microservice's service account and its associated IAM bindings. | <pre>list(object({<br>    sa_name          = string<br>    use_common_roles = bool<br>    additional_roles = list(string)<br>  }))</pre> | `[]` | no |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | project ID | `string` | n/a | yes |
## Outputs

| Name | Description |
|------|-------------|
| <a name="output_gke_pod_microservices_sa_emails"></a> [gke\_pod\_microservices\_sa\_emails](#output\_gke\_pod\_microservices\_sa\_emails) | Service Account Email for each microservice |

<!-- END_TF_DOCS -->
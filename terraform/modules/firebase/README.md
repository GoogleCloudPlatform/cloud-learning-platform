## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google-beta_google_firebase_project.default](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_firebase_project) | resource |
| [google-beta_google_firebase_web_app.ai-tutor](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_firebase_web_app) | resource |
| [google-beta_google_firebase_web_app.ckt](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/google_firebase_web_app) | resource |
| [google_app_engine_application.app](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/app_engine_application) | resource |
| [google_cloudbuild_trigger.ai-tutor](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudbuild_trigger) | resource |
| [google_cloudbuild_trigger.ckt](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudbuild_trigger) | resource |
| [google_cloudbuild_trigger.firebase-builder](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudbuild_trigger) | resource |
| [google_project_iam_member.cloud-build-firebase-admin](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_iam_member) | resource |
| [google-beta_google_firebase_web_app_config.ai-tutor](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/data-sources/google_firebase_web_app_config) | data source |
| [google-beta_google_firebase_web_app_config.ckt](https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/data-sources/google_firebase_web_app_config) | data source |
| [google_project.project](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_ai_tutor_whitelist_domains"></a> [ai\_tutor\_whitelist\_domains](#input\_ai\_tutor\_whitelist\_domains) | Comma separated list of email domains that should have access to AI Tutor | `string` | n/a | yes |
| <a name="input_ai_tutor_whitelist_emails"></a> [ai\_tutor\_whitelist\_emails](#input\_ai\_tutor\_whitelist\_emails) | Comma separated list of individual emails that should have access to AI Tutor | `string` | n/a | yes |
| <a name="input_ckt_whitelist_domains"></a> [ckt\_whitelist\_domains](#input\_ckt\_whitelist\_domains) | Comma separated list of email domains that should have access to CKT | `string` | n/a | yes |
| <a name="input_ckt_whitelist_emails"></a> [ckt\_whitelist\_emails](#input\_ckt\_whitelist\_emails) | Comma separated list of individual emails that should have access to CKT | `string` | n/a | yes |
| <a name="input_ckt_okta_login"></a> [ckt\_whitelist\_emails](#input\_ckt\_whitelist\_emails) | Support OKTA login in CKT | `bool` | n/a | yes |
| <a name="input_ckt_pp_assessments"></a> [ckt\_whitelist\_emails](#input\_ckt\_whitelist\_emails) | Enable Paraphrase assessments in CKT | `bool` | n/a | yes |
| <a name="input_ckt_ckn_assessments"></a> [ckt\_whitelist\_emails](#input\_ckt\_whitelist\_emails) | Enable Create Knowledge Notes assessments in CKT | `bool` | n/a | yes |
| <a name="input_firestore_region"></a> [firestore\_region](#input\_firestore\_region) | Firestore Region - must be app\_engine region | `string` | n/a | yes |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | GCP Project ID | `string` | `"aitutor-dev"` | no |

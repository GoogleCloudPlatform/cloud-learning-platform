## Requirements

No requirements.

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_cloud-nat"></a> [cloud-nat](#module\_cloud-nat) | terraform-google-modules/cloud-nat/google | ~> 1.2 |
| <a name="module_vpc"></a> [vpc](#module\_vpc) | terraform-google-modules/network/google | ~> 4.0 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_create_router"></a> [create\_router](#input\_create\_router) | create router True/False | `bool` | n/a | yes |
| <a name="input_nat_log_config_enable"></a> [nat\_log\_config\_enable](#input\_nat\_log\_config\_enable) | nat log config enabling and disabling | `bool` | n/a | yes |
| <a name="input_nat_log_config_filter"></a> [nat\_log\_config\_filter](#input\_nat\_log\_config\_filter) | nat log config filter to filter the log level | `string` | n/a | yes |
| <a name="input_nat_name"></a> [nat\_name](#input\_nat\_name) | nat name | `string` | n/a | yes |
| <a name="input_nat_router_name"></a> [nat\_router\_name](#input\_nat\_router\_name) | nat router name | `string` | n/a | yes |
| <a name="input_nat_router_region"></a> [nat\_router\_region](#input\_nat\_router\_region) | nat router region | `string` | n/a | yes |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | specify the project name | `string` | n/a | yes |
| <a name="input_secondary_ranges"></a> [secondary\_ranges](#input\_secondary\_ranges) | specify the secondary ranges | <pre>map(list(object(<br>  {<br>    range_name    = string,<br>    ip_cidr_range = string<br>  }<br>)))</pre> | n/a | yes |
| <a name="input_subnets"></a> [subnets](#input\_subnets) | specify the subnet details | `list(map(string))` | n/a | yes |
| <a name="input_vpc_network"></a> [vpc\_network](#input\_vpc\_network) | specify the vpc name | `string` | n/a | yes |

## Outputs

No outputs.

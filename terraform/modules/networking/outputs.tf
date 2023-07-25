# network and subnetwork self links are used as input to create a bastion host
output "network_self_link" {
  value       = module.vpc.network_self_link
  description = "The URI of the VPC being created"
}

output "subnets_self_link" {
  value       = module.vpc.subnets_self_links
  description = "The URI of the VPC subnetworks being created"
}

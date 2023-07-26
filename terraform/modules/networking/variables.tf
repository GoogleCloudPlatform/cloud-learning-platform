variable "vpc_network" {
  type        = string
  description = "specify the vpc name"
}

variable "project_id" {
  type        = string
  description = "specify the project name"
}

# Cloud NAT variables

variable "region" {
  type        = string
  description = "nat router region"
}

variable "environment" {
  type        = string
  description = "The environment context"
}

variable "project" {
  type        = string
  description = "The project name"
}

variable "resource_group_name" {
  type        = string
  description = "The resource group where the app service resources will be created"
}

variable "location" {
  type        = string
  description = "The location resources should be provisioned withins"
}

variable "sku_name" {
  type        = string
  description = "The SKU name of the app service plan"
}

variable "os_type" {
  type        = string
  description = "The OS type of the app service plan"
}

variable "docker_registry_name" {
  type = string
}

variable "docker_registry_username" {
  type        = string
  description = "The username to use for the Docker registry auth"
  sensitive   = true
}

variable "docker_registry_password" {
  type        = string
  description = "The password to use for the Docker registry auth"
  sensitive   = true
}

variable "apps" {
  description = "The apps to be deployed in to App Services"
}

variable "user_assigned_identity" {
  type    = string
  default = null
}

variable "user_assigned_client_identity" {
  type    = string
  default = ""
}

variable "allowed_inbound_ips" {
  type      = list(string)
  default   = [""]
  sensitive = true
}

variable "key_vault_id" {
  type = string
}

variable "log_analytics_workspace_id" {
  type = string
}

variable "dns_zone_name" {
  type    = string
  default = ""
}

variable "dns_resource_group_name" {
  type    = string
  default = ""
}

variable "auth_settings" {
  type    = map(any)
  default = {}
}

variable "tags" {
  description = "Tags that should be applied to resources created by this module. Runtime tag values will take precedent over compile time values"
  type        = map(string)
  default     = {}
}

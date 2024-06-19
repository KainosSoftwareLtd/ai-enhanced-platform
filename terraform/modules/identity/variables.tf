variable "resource_group_name" {
  description = "The resource group where the identity resources will be created"
}

variable "location" {
  description = "The region where you are deploying the identity resources"
}

variable "environment" {
  description = "The environment type i.e. stable, feature, prod"
}

variable "project" {
  description = "The project context"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags that will be applied to all resources provisioned."
}

variable "key_vault_id" {
  type        = string
  description = "Reference to the KV instance"
}

variable "identity_kv_permissions" {
  description = "Define the list of accepted permissions"
  type = map(object({
    secret_permissions      = list(string)
    certificate_permissions = list(string)
    key_permissions         = list(string)
  }))
}
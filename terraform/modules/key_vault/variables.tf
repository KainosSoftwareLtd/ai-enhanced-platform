variable "environment" {
  type        = string
  description = "The environment context"
}

variable "project" {
  type        = string
  description = "The project name"
}

variable "location" {
  type        = string
  description = "The location of the key vault"
}

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group"
}

variable "soft_delete_retention" {
  type        = number
  description = "days to retain soft deleted objects"
}

variable "purge_protection_enabled" {
  type        = bool
  description = "Purge protection enabled / disabled"
}

variable "sku_name" {
  type        = string
  description = "The SKU of the Key Vault"
}

variable "app_service_entra_id" {
  type        = string
  description = "The entra id for your app service"
}

variable "tags" {
  type        = map(string)
  description = "Tags that should be applied to resources created by this module. Runtime tag values will take precedent over compile time values"
  default     = {}
}

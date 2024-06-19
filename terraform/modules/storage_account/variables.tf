variable "environment" {
  type        = string
  description = "The environment context"
}

variable "name" {
  type        = string
  description = "The name of the datastore component"
}

variable "location" {
  type = string
}

variable "project" {
  type        = string
  description = "The project context"
}

variable "resource_group_name" {
  type        = string
  description = "The resource group where the storage account resources will be created"
}

variable "tags" {
  description = "Tags that should be applied to resources created by this module. Runtime tag values will take precedent over compile time values"
  type        = map(string)
  default     = {}
}

variable "network_rules_enabled" {
  description = "Enabled if network_rules block is to be declared for storage account"
  type        = string
  default     = null
}

variable "storage_containers" {
  description = "All storage containers"
  type        = list(string)
  default     = []
}

variable "storage_shares" {
  description = "All storage containers"
  type        = list(string)
  default     = []
}

variable "storage_share_max_size" {
  description = "The maximum size of the file share"
  type        = number
  default     = 256
}

variable "account_tier" {
  description = "Sets argument account_tier of the storage account (Standard/Premium). Changing this forces a new resource to be created."
  type        = string
  default     = "Standard"
}

variable "access_tier" {
  description = "Sets argument access_tier of the storage account (Hot/Cool) defaults to Hot"
  type        = string
  default     = "Hot"
}

variable "account_kind" {
  description = "Sets argument account_kind of the storage account (BlobStorage/BlockBlobStorage/FileStorage/Storage/StorageV2)"
  type        = string
  default     = "StorageV2"
}

variable "account_replication_kind" {
  description = "Sets argument account_replication_kind of the storage account (LRS/GRS/RAGRS/ZRS/GZRS/RAGZRS)"
  type        = string
  default     = "RAGRS"
}

variable "enable_https_traffic_only" {
  description = "Sets argument enable_https_traffic_only of the storage account (true/fals)"
  type        = bool
  default     = true
}

variable "allow_nested_items_to_be_public" {
  description = "Sets argument allow_nested_items_to_be_public of the storage account (true/false)"
  type        = bool
  default     = false
}

variable "kv_content_type" {
  description = "Sets content_type argument of the key vault secret"
  type        = string
  default     = null
}

variable "sc_name" {
  description = "Names of the created storage containers"
  type        = string
  default     = null
}

variable "container_access_type" {
  description = "Type of acces for the container (blob/container/private)"
  type        = string
  default     = "private"
}


variable "public_network_access_enabled" {
  description = "Sets argument public_network_access_enabled of the storage account (true/false)"
  type        = bool
  default     = true
}

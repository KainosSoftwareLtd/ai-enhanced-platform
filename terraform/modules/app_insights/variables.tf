variable "resource_group_name" {
  type        = string
  description = "The name of the resource group the application insights will be deployed to "
}

variable "environment" {
  type        = string
  description = "The environment the app insights resource will be deployed to"
}

variable "project" {
  type        = string
  description = "The name of the project the app insights resource will be deployed to"
}

variable "location" {
  type        = string
  description = "The location the application insights will be deployed to"
}

variable "log_analytics_workspace_id" {
  type        = string
  description = "The id of the log analytics workspace that the app insights will be linked to"

}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags that should be applied to the resources created by this module"
}
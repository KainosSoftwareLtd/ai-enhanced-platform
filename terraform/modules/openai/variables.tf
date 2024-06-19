variable "location" {
  default = "westeurope"
}

variable "resource_group_name" {
  type = string
}

variable "app_name" {
}

variable "environment" {
}

variable "region" {
}

variable "instance_number" {
}

variable "openai_deployments" {
  type = map(object({
    name            = string
    model_format    = string
    model_name      = string
    model_version   = string
    scale_type      = string
    capacity        = string
    rai_policy_name = optional(string)
  }))
  default     = {}
  description = <<-DESCRIPTION
      type = map(object({
        name                 = (Required) The name of the Cognitive Services Account Deployment. Changing this forces a new resource to be created.
        cognitive_account_id = (Required) The ID of the Cognitive Services Account. Changing this forces a new resource to be created.
        model = {
          model_format  = (Required) The format of the Cognitive Services Account Deployment model. Changing this forces a new resource to be created. Possible value is OpenAI.
          model_name    = (Required) The name of the Cognitive Services Account Deployment model. Changing this forces a new resource to be created.
          model_version = (Required) The version of Cognitive Services Account Deployment model.
        }
        scale = {
          scale_type = (Required) Deployment scale type. Possible value is Standard. Changing this forces a new resource to be created.
          capacity   = (Required) The capacity of the Cognitive Services Account Deployment. (Defaults to 1 which means that the limitation is 1000 tokens per minute) Changing this forces a new resource to be created.
        }
        rai_policy_name = (Optional) The name of RAI policy. Changing this forces a new resource to be created.
      }))
  DESCRIPTION
  nullable    = false
}

variable "private_dns_zone_ids" {
  description = "Specifies the list of Private DNS Zones to include within the private_dns_zone_group."
  type        = list(string)
  default     = []
}

variable "subnet_id" {
  description = "Specifies the resource id of the subnet"
  type        = string
  default     = ""
}

variable "enable_private_endpoint" {
  default = true
}

variable "log_analytics_workspace_id" {
}

variable "log_analytics_retention_days" {
}

variable "tags" {
  type = map(string)
  default = {
    environment = "dev"
  }
}
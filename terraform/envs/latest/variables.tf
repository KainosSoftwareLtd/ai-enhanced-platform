variable "location" {
  type    = string
  default = "uksouth"
}

variable "project" {
  type    = string
  default = "aep"
}

variable "environment" {
  type    = string
  default = "latest"
}

variable "image_tag" {
  type    = string
  default = "main"
}

variable "system_api_key" {
  type        = string
  description = "The Azure System API key to use for the service"
  sensitive   = true
}

variable "allowed_inbound_ips" {
  type      = list(string)
  default   = [""]
  sensitive = true
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

variable "openai_deployments" {
  type = map(object({
    name            = string
    model_format    = string
    model_name      = string
    model_version   = string
    scale_type      = string
    rai_policy_name = optional(string)
  }))
  default = {
    "model" = {
      name            = "gpt-35-turbo"
      model_format    = "OpenAI"
      model_name      = "gpt-35-turbo"
      model_version   = "1106"
      scale_type      = "Standard"
      rai_policy_name = "defaultcontentpolicy"
    }
  }
}

locals {
  tags = {
    project     = var.project
    environment = var.environment
    datetime    = timestamp()
  }

  identity_kv_permissions = {
    aas = {
      secret_permissions = [
        "Get",
        "List"
      ]
      certificate_permissions = [
      ]
      key_permissions = [
      ]
    }
  }

  apps = {
    service = {
      name              = "api-service"
      docker_image_name = "kainossoftwareltd/ai-enhanced-platform:${var.image_tag}"

      app_vars = {
        OPENAI_API_KEY                             = module.openai.openai_primary_access_key
        OPENAI_API_TYPE                            = "azure"
        OPENAI_MODEL                               = var.openai_deployments["model"].name
        AZURE_OPENAI_ENDPOINT                      = module.openai.openai_endpoint
        SYSTEM_API_KEY                             = var.system_api_key
        AZURE_VAULT_ID                             = module.key_vault.key_vault_uri
        AZURE_CLIENT_ID                            = module.identity.identities["aas"].client_id
        WEBSITES_PORT                              = "8000"
        DOCKER_REGISTRY_SERVER_USERNAME            = var.docker_registry_username
        DOCKER_REGISTRY_SERVER_PASSWORD            = var.docker_registry_password
        AZURE_CS_ENDPOINT                          = module.openai.cs_endpoint
        AZURE_CS_KEY                               = module.openai.cs_primary_access_key
        APPINSIGHTS_KEY                            = module.app_insights.instrumentation_key
        APPINSIGHTS_PROFILERFEATURE_VERSION        = "1.0.0"
        APPINSIGHTS_SNAPSHOTFEATURE_VERSION        = "1.0.0"
        APPLICATIONINSIGHTS_CONNECTION_STRING      = "InstrumentationKey=${module.app_insights.instrumentation_key}"
        ApplicationInsightsAgent_EXTENSION_VERSION = "~3"
        OTEL_RESOURCE_ATTRIBUTES                   = "aep-${var.environment}-${var.image_tag}"
        OTEL_SERVICE_NAME                          = "aep-${var.environment}-${var.image_tag}"
        OTEL_LIVE_METRICS_ENABLED                  = var.otel_live_metrics_enabled
        OTEL_DISABLE_OFFLINE_STORAGE               = var.otel_disable_offline_storage
        OTEL_TRACES_SAMPLER                        = var.otel_traces_sampler
      }

      storage_account = {
        name         = "log-output"
        type         = "AzureFiles"
        share_name   = "logs"
        mount_path   = "/app/logs"
        account_name = module.logging_storageaccount.storage_account_name
        access_key   = module.logging_storageaccount.primary_access_key
      }

      health_check_path = "/healthcheck"
    }
  }
}

resource "azurerm_resource_group" "rg" {
  name     = format("rg-%s-%s-%s", var.project, var.environment, var.location)
  location = var.location
}

resource "azurerm_consumption_budget_resource_group" "budget" {
  name              = "budget"
  resource_group_id = azurerm_resource_group.rg.id

  amount     = 100
  time_grain = "Monthly"

  time_period {
    start_date = "2024-04-01T00:00:00Z"
    end_date   = "2025-04-01T00:00:00Z"
  }

  notification {
    enabled        = true
    threshold      = 90.0
    operator       = "EqualTo"
    threshold_type = "Actual"

    contact_emails = [
    ]
  }
}

module "app_service" {
  source                   = "../../modules/app_services"
  environment              = var.environment
  project                  = var.project
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku_name                 = "B2"
  os_type                  = "Linux"
  apps                     = local.apps
  docker_registry_name     = "https://ghcr.io"
  docker_registry_username = var.docker_registry_username
  docker_registry_password = var.docker_registry_password
  allowed_inbound_ips      = var.allowed_inbound_ips
  key_vault_id             = module.key_vault.key_vault_id
  user_assigned_identity   = module.identity.identities["aas"].id

  tags = local.tags
}

module "key_vault" {
  source                   = "../../modules/key_vault"
  environment              = var.environment
  project                  = var.project
  purge_protection_enabled = true
  soft_delete_retention    = 7
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku_name                 = "standard"
  app_service_entra_id     = module.app_service.app_service_id

  tags = local.tags
}

module "logging_storageaccount" {
  source                          = "../../modules/storage_account"
  location                        = azurerm_resource_group.rg.location
  resource_group_name             = azurerm_resource_group.rg.name
  environment                     = var.environment
  name                            = "logging"
  tags                            = local.tags
  project                         = var.project
  storage_shares                  = ["logs"]
  account_tier                    = "Standard"
  access_tier                     = "Hot"
  account_kind                    = "StorageV2"
  account_replication_kind        = "LRS"
  enable_https_traffic_only       = "true"
  allow_nested_items_to_be_public = "false"
  container_access_type           = "private"
}

module "identity" {
  source                  = "../../modules/identity"
  resource_group_name     = azurerm_resource_group.rg.name
  location                = azurerm_resource_group.rg.location
  environment             = var.environment
  project                 = var.project
  tags                    = local.tags
  key_vault_id            = module.key_vault.key_vault_id
  identity_kv_permissions = local.identity_kv_permissions
}

module "log_analytics" {
  source = "../../modules/log_analytics"

  app_name        = "la"
  environment     = var.environment
  instance_number = "01"
  region          = "uks"

  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  depends_on = [
    azurerm_resource_group.rg
  ]

}

module "app_insights" {
  source                     = "../../modules/app_insights"
  environment                = var.environment
  project                    = var.project
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  log_analytics_workspace_id = module.log_analytics.log_analytics_id

  tags = local.tags
}

module "openai" {
  source          = "../../modules/openai"
  app_name        = "openaipoc"
  environment     = var.environment
  instance_number = "01"
  region          = "uks"

  openai_deployments = {
    "gpt_35_turbo" = {
      name            = "gpt-35-turbo"
      model_format    = "OpenAI"
      model_name      = "gpt-35-turbo"
      model_version   = "1106"
      scale_type      = "Standard"
      capacity        = "121"
      rai_policy_name = "defaultcontentpolicy"
    },
    "gpt_4_turbo" = {
      name            = "gpt-4-turbo"
      model_format    = "OpenAI"
      model_name      = "gpt-4"
      model_version   = "0125-Preview"
      scale_type      = "Standard"
      capacity        = "80"
      rai_policy_name = "defaultcontentpolicy"
    }
  }

  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  tags = local.tags

  log_analytics_workspace_id   = module.log_analytics.log_analytics_id
  log_analytics_retention_days = module.log_analytics.retention_in_days

  depends_on = [
    azurerm_resource_group.rg,
    module.log_analytics
  ]

}

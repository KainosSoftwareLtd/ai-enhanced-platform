resource "azurerm_service_plan" "plan" {
  name                = format("plan-%s-%s-%s", var.environment, var.project, var.location)
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags

  sku_name = var.sku_name
  os_type  = var.os_type
}

resource "azurerm_linux_web_app" "apps" {
  for_each            = var.apps
  name                = format("app-%s-%s-%s-%s", var.project, substr(each.value.name, 0, 5), var.environment, var.location)
  resource_group_name = var.resource_group_name
  location            = azurerm_service_plan.plan.location
  service_plan_id     = azurerm_service_plan.plan.id
  tags                = var.tags

  # Update the app settings every time to force a restart
  app_settings = merge(each.value.app_vars, { "RESTART_TIMESTAMP" = timestamp() })

  site_config {
    ftps_state        = "Disabled"
    always_on         = "true"
    health_check_path = each.value.health_check_path

    application_stack {
      docker_image_name        = each.value.docker_image_name
      docker_registry_url      = var.docker_registry_name
      docker_registry_username = var.docker_registry_username
      docker_registry_password = var.docker_registry_password
    }
  }

  dynamic "storage_account" {
    for_each = [for k, v in local.app_service_mounted_storage_references : v if v.service == each.key]
    content {
      name         = storage_account.value["name"]
      type         = storage_account.value["type"]
      account_name = storage_account.value["account_name"]
      share_name   = storage_account.value["share_name"]
      access_key   = storage_account.value["access_key"]
      mount_path   = storage_account.value["mount_path"]
    }
  }

  key_vault_reference_identity_id = var.user_assigned_identity
  identity {
    type         = "UserAssigned"
    identity_ids = [var.user_assigned_identity]
  }
}

# Add diagnostic settings to the app services
resource "azurerm_monitor_diagnostic_setting" "app_services" {
  for_each                   = azurerm_linux_web_app.apps
  name                       = format("diag-%s", each.key)
  target_resource_id         = each.value.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  log {
    category = "AppServiceHTTPLogs"
    enabled  = true
  }

  log {
    category = "AppServiceConsoleLogs"
    enabled  = true
  }

  log {
    category = "AppServiceAppLogs"
    enabled  = true
  }

  log {
    category = "AppServicePlatformLogs"
    enabled  = true
  }

  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

# Add the certificates required for the custom domains
data "azurerm_key_vault_certificate" "certs" {
  for_each     = local.app_service_records
  name         = each.value.certificate
  key_vault_id = var.key_vault_id
}

# Add the certificates required for the custom domains, the KV reference should match the subdomain i.e. stubs, auth-stubs, ag-stubs
resource "azurerm_app_service_certificate" "certs" {
  for_each = data.azurerm_key_vault_certificate.certs
  # We use the subdomain references to pull 
  name                = "${each.value.name}-${each.key}"
  resource_group_name = var.resource_group_name
  location            = var.location
  key_vault_secret_id = each.value.id
  tags                = var.tags
}

# Add the CNAME references for each of the subdomains required for the mock service
resource "azurerm_dns_cname_record" "hostnames" {
  for_each            = local.app_service_records
  name                = each.value.hostname
  zone_name           = var.dns_zone_name
  resource_group_name = var.dns_resource_group_name
  ttl                 = 300
  record              = azurerm_linux_web_app.apps[each.value.service].default_hostname
  tags                = var.tags
}

resource "azurerm_app_service_custom_hostname_binding" "certs" {
  depends_on          = [azurerm_app_service_certificate.certs, azurerm_dns_cname_record.hostnames]
  for_each            = local.app_service_records
  hostname            = "${each.value.hostname}.${var.dns_zone_name}"
  app_service_name    = azurerm_linux_web_app.apps[each.value.service].name
  resource_group_name = var.resource_group_name
  ssl_state           = "SniEnabled"
  thumbprint          = data.azurerm_key_vault_certificate.certs[each.key].thumbprint
}

locals {
  # This generates objects for each app that requires a mounted storage reference and resolves the
  # access key that it needs to authorize requests
  app_service_mounted_storage_references = { for k, v in var.apps : format("%s-%s", k, v.storage_account.name) => {
    service      = k
    name         = v.storage_account.name
    type         = v.storage_account.type
    account_name = v.storage_account.account_name
    share_name   = v.storage_account.share_name
    access_key   = v.storage_account.access_key
    mount_path   = v.storage_account.mount_path
  } if can(v.storage_account) }

  app_service_records = { for k, v in var.apps : format("%s-%s", k, v.records.hostname) => {
    service     = k
    hostname    = v.records.hostname
    certificate = v.records.certificate
  } if can(v.records) }

  auth_settings = merge({
    auth_enabled = false
  }, var.auth_settings)
}

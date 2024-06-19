data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "keyvault" {
  name                       = format("vault-%s-%s-%s", var.environment, substr(var.project, 0, 5), substr(var.location, 0, 3))
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = var.soft_delete_retention
  purge_protection_enabled   = var.purge_protection_enabled
  tags                       = var.tags

  sku_name = var.sku_name
}

resource "azurerm_key_vault_access_policy" "keyvaultap" {
  key_vault_id = azurerm_key_vault.keyvault.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  key_permissions = ["Get", "List",
    "Delete", "Create",
    "Import", "Backup",
  "Restore", "Recover"]

  secret_permissions = ["Get", "List", "Set",
    "Delete", "Backup",
  "Restore", "Recover"]
}

locals {
  shortLocation = substr(var.location, 0, 3)
}

resource "azurerm_storage_account" "storage_account" {
  name                            = lower(format("st%s%s%s%s", var.project, var.name, var.environment, local.shortLocation))
  resource_group_name             = var.resource_group_name
  location                        = var.location
  account_tier                    = var.account_tier
  access_tier                     = var.access_tier
  account_kind                    = var.account_kind
  account_replication_type        = var.account_replication_kind
  enable_https_traffic_only       = var.enable_https_traffic_only
  allow_nested_items_to_be_public = var.allow_nested_items_to_be_public
  public_network_access_enabled   = var.public_network_access_enabled
}

resource "azurerm_storage_container" "sc" {
  for_each              = toset(var.storage_containers)
  name                  = each.key
  storage_account_name  = azurerm_storage_account.storage_account.name
  container_access_type = var.container_access_type
}

# Create a fileshare within the storage account
resource "azurerm_storage_share" "ss" {
  for_each             = toset(var.storage_shares)
  name                 = each.key
  storage_account_name = azurerm_storage_account.storage_account.name
  quota                = var.storage_share_max_size
}
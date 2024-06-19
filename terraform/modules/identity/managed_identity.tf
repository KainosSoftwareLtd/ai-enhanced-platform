resource "azurerm_user_assigned_identity" "user_assigned_identity" {
  for_each = var.identity_kv_permissions

  location            = var.location
  resource_group_name = var.resource_group_name
  name                = "mi-${var.project}-${each.key}-${var.environment}-${var.location}"
  tags                = var.tags
}
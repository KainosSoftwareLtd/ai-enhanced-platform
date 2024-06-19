resource "azurerm_key_vault_access_policy" "kv_access_policy" {
  for_each = var.identity_kv_permissions

  key_vault_id = var.key_vault_id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.user_assigned_identity[each.key].principal_id

  secret_permissions      = each.value.secret_permissions
  certificate_permissions = each.value.certificate_permissions
  key_permissions         = each.value.key_permissions
}
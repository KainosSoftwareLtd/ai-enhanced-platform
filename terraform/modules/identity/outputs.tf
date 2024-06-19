output "identities" {
  description = "Output the user assigned identity from the module"
  value       = azurerm_user_assigned_identity.user_assigned_identity
}
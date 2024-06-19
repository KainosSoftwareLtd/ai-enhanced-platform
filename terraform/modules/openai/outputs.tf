output "openai_id" {
  value = azurerm_cognitive_account.cognitive_account.id
}

output "openai_endpoint" {
  value       = azurerm_cognitive_account.cognitive_account.endpoint
  description = "Specifies the endpoint of the Azure OpenAI Service."
}

output "openai_primary_access_key" {
  value       = azurerm_cognitive_account.cognitive_account.primary_access_key
  description = "Specifies the primary access key of the Azure OpenAI Service."
  sensitive   = true
}

output "openai_secondary_access_key" {
  value       = azurerm_cognitive_account.cognitive_account.secondary_access_key
  description = "Specifies the secondary access key of the Azure OpenAI Service."
  sensitive   = true
}

output "name" {
  value = azurerm_cognitive_account.cognitive_account.name
}

output "cs_endpoint" {
  value       = azurerm_cognitive_account.content_safety.endpoint
  description = "Specifies the endpoint of the Azure OpenAI Service."
}

output "cs_primary_access_key" {
  value       = azurerm_cognitive_account.content_safety.primary_access_key
  description = "Specifies the primary access key of the Azure OpenAI Service."
  sensitive   = true
}

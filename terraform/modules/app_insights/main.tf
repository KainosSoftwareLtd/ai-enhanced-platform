data "azurerm_log_analytics_workspace" "aep-analytics" {
  name                = format("law-la-%s-%s-%s-01", var.project, var.environment, var.environment)
  resource_group_name = "rg-gippi-latest-uksouth"
}
resource "azurerm_application_insights" "aep_insights" {
  name                = format("insights-%s-%s-%s", var.project, var.environment, var.location)
  location            = var.location
  resource_group_name = var.resource_group_name
  workspace_id        = data.azurerm_log_analytics_workspace.aep-analytics.id
  application_type    = "web"
}

output "instrumentation_key" {
  value = azurerm_application_insights.aep_insights.instrumentation_key
}

output "app_insights_id" {
  value = azurerm_application_insights.aep_insights.id
}
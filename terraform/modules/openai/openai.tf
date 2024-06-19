resource "azurerm_cognitive_account" "cognitive_account" {

  location = var.location

  name = format("oai-%s-%s-%s-%s",
    var.app_name,
    var.environment,
    var.region,
    var.instance_number
  )

  custom_subdomain_name = format("oai-%s-%s-%s-%s",
    var.app_name,
    var.environment,
    var.region,
    var.instance_number
  )

  resource_group_name = var.resource_group_name

  kind     = "OpenAI"
  sku_name = "S0"

  local_auth_enabled                 = true
  outbound_network_access_restricted = false
  public_network_access_enabled      = true

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.oai_identity.id]
  }

}

resource "azurerm_cognitive_account" "content_safety" {

  location = "westeurope"

  name = format("cs-%s-%s-%s-%s",
    var.app_name,
    var.environment,
    var.region,
    var.instance_number
  )

  custom_subdomain_name = format("cs-%s-%s-%s-%s",
    var.app_name,
    var.environment,
    var.region,
    var.instance_number
  )

  resource_group_name = var.resource_group_name

  kind     = "ContentSafety"
  sku_name = "S0"

  local_auth_enabled                 = true
  outbound_network_access_restricted = false
  public_network_access_enabled      = true

}

resource "azurerm_user_assigned_identity" "oai_identity" {
  location = var.location

  name = format("oai-mi-%s-%s-%s-%s",
    var.app_name,
    var.environment,
    var.region,
    var.instance_number
  )

  resource_group_name = var.resource_group_name

  tags = var.tags

}

resource "azurerm_cognitive_deployment" "cognitive_deployment" {
  for_each = var.openai_deployments

  cognitive_account_id = azurerm_cognitive_account.cognitive_account.id
  name                 = each.value.name
  rai_policy_name      = each.value.rai_policy_name

  model {
    format  = each.value.model_format
    name    = each.value.model_name
    version = each.value.model_version
  }
  scale {
    type     = each.value.scale_type
    capacity = each.value.capacity
  }
}

resource "azapi_resource" "content_filtering_policy" {
  type      = "Microsoft.CognitiveServices/accounts/raiPolicies@2023-10-01-preview"
  name      = "defaultcontentpolicy"
  parent_id = azurerm_cognitive_account.cognitive_account.id

  schema_validation_enabled = false

  body = jsonencode({
    properties = {
      mode           = "Default",
      basePolicyName = "Microsoft.Default",
      contentFilters = [
        { name = "hate", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
        { name = "sexual", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
        { name = "selfharm", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
        { name = "violence", blocking = true, enabled = true, allowedContentLevel = "High", source = "Prompt" },
        { name = "hate", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
        { name = "sexual", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
        { name = "selfharm", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
        { name = "violence", blocking = true, enabled = true, allowedContentLevel = "High", source = "Completion" },
        { name = "jailbreak", blocking = true, enabled = true, source = "Prompt" },
        { name = "protected_material_text", blocking = true, enabled = true, source = "Completion" },
        { name = "protected_material_code", blocking = true, enabled = true, source = "Completion" }
      ]
    }
  })
}
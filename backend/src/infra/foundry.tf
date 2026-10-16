resource "azurerm_cognitive_account" "foundry" {
  name                               = "foundry-enterprise-ai-${var.prefix}"
  location                           = azurerm_resource_group.rg.location
  resource_group_name                = azurerm_resource_group.rg.name
  kind                               = "AIServices"
  sku_name                           = "S0"
  project_management_enabled         = true
  custom_subdomain_name              = "foundry-enterprise-ai-${var.prefix}"
  local_auth_enabled                 = true # false # true
  public_network_access_enabled      = true
  outbound_network_access_restricted = false

  identity {
    type = "SystemAssigned"
  }

  tags = {
    SecurityControl = "Ignore"
  }
}

# Assign the Foundry User role on your Foundry resource to your user principal.
resource "azurerm_role_assignment" "foundry_user" {
  scope                = azurerm_cognitive_account.foundry.id
  role_definition_name = "Foundry User"
  principal_id         = data.azurerm_client_config.current.object_id
}

data "azurerm_client_config" "current" {}

output "foundry_endpoint" {
  value = var.foundry_endpoint
}

output "foundry_api_key" {
  value     = var.foundry_api_key
  sensitive = true
}
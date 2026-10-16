resource "azurerm_resource_group" "rg" {
  name     = "rg-enterprise-ai-operations-${var.prefix}"
  location = "southeastasia"
}
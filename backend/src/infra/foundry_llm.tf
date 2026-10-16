
resource "azurerm_cognitive_deployment" "gpt_54" {
  name                 = "gpt-5.4"
  cognitive_account_id = azurerm_cognitive_account.foundry.id

  sku {
    name     = "GlobalStandard" # "Standard" # DataZoneStandard, GlobalBatch, GlobalStandard and ProvisionedManaged
    capacity = 1000
  }

  model {
    format  = "OpenAI"
    name    = "gpt-5.4"
    version = "2026-03-05"
  }
}

output "llm_model_deployment_name_chatgpt" {
  value = var.llm_model_deployment_name_chatgpt
}

output "llm_model_deployment_name" {
  value = var.llm_model_deployment_name
}

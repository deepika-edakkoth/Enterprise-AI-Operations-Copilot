variable "prefix" {
  description = "Prefix for all resources in this project"
  type        = string
  default     = "001"
}

variable "foundry_endpoint" {
  default     = "https://foundry-deepika-001.cognitiveservices.azure.com/"
  type        = string
}

variable "foundry_api_key" {
  type        = string
  sensitive   = true
}

variable "llm_model_deployment_name" {
  type = string
}

variable "foundry_project_endpoint" {
  type = string
}

variable "llm_model_deployment_name_chatgpt" {
  type = string
}
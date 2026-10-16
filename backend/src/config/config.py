import subprocess

print("Loading config...")

def get_terraform_output(name: str) -> str:
    result = subprocess.run(
        ["terraform", "-chdir=infra", "output", "-raw", name],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# Retrieve values from Terraform
FOUNDRY_ENDPOINT = get_terraform_output("foundry_endpoint")
FOUNDRY_API_KEY = get_terraform_output("foundry_api_key")
LLM_MODEL_DEPLOYMENT_NAME = get_terraform_output("llm_model_deployment_name")
COSMOSDB_ENDPOINT = get_terraform_output("cosmosdb_endpoint")
COSMOSDB_KEY = get_terraform_output("cosmosdb_key")


#Langsmith API Key
LANGSMITH_API_KEY = "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"
LANGSMITH_PROJECT = "enterprise_ai_operations"

# For security, only print partial API key
if FOUNDRY_API_KEY:
    print("Foundry API Key:", f"{FOUNDRY_API_KEY[-10:]}...")
print("Foundry Endpoint:", FOUNDRY_ENDPOINT)
print("LLM Model Deployment Name:", LLM_MODEL_DEPLOYMENT_NAME)
print("CosmosDB Endpoint:", COSMOSDB_ENDPOINT)
if COSMOSDB_KEY:
    print("CosmosDB Key:", COSMOSDB_KEY[:10] + "...")

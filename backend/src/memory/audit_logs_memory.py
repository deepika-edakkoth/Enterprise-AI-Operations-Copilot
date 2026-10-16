from langchain_azure_cosmosdb import CosmosDBSaverSync
import config.config as config

class AuditLogsMemoryClient:
    def __init__(self):
        self.audit_logger = CosmosDBSaverSync(
            database_name="enterprise-ai-memory",
            container_name="audit_logs",
            endpoint=config.COSMOSDB_ENDPOINT,
            key=config.COSMOSDB_KEY,
        )
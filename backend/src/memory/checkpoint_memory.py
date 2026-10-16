from azure.cosmos.aio import CosmosClient
from langchain_azure_cosmosdb import CosmosDBSaver
from azure.cosmos import PartitionKey
import config.config as config


class CheckpointMemoryClient:

    def __init__(self):
        self.client = None
        self.checkpointer = None

    async def initialize(self):

        print("Initializing Checkpointer...")

        self.client = CosmosClient(
            config.COSMOSDB_ENDPOINT,
            config.COSMOSDB_KEY
        )

        database = await self.client.create_database_if_not_exists(
            id="enterprise-ai-memory"
        )

        container = await database.create_container_if_not_exists(
            id="checkpoints",
            partition_key=PartitionKey(path="/thread_id")
        )

        self.checkpointer = CosmosDBSaver(
            container=container
        )

        print("Checkpointer initialized successfully.")

    async def close(self):
        """Close the Azure Cosmos DB asynchronous client."""
        if self.client is not None:
            await self.client.close()
            self.client = None
            self.checkpointer = None
            print("Checkpoint client closed.")

memory_client = CheckpointMemoryClient()
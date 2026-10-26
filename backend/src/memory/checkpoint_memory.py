from azure.cosmos.aio import CosmosClient
from langchain_azure_cosmosdb import CosmosDBSaver
from azure.cosmos import PartitionKey
import config.config as config


class CheckpointMemoryClient:

    def __init__(self):
        self.client = None
        self.database = None
        self.conversations_container = None
        self.checkpointer = None
        self.ticket_container = None
        # We store the context manager wrapper so we can properly close it later
        self._checkpointer_ctx = None

    async def initialize(self):

        print("Initializing Checkpointer...")

        self.client = CosmosClient(
            config.COSMOSDB_ENDPOINT,
            config.COSMOSDB_KEY
        )
         # Open the client's internal session transport
        await self.client.__aenter__()

        self.database = await self.client.create_database_if_not_exists(
            id="enterprise-ai-memory"
        )

        #checkpoints_container = 
        await self.database.create_container_if_not_exists(
            id="checkpoints",
            partition_key=PartitionKey(path="/partition_key")
        )

        self.conversations_container = await self.database.create_container_if_not_exists(
            id="conversations",
            partition_key=PartitionKey(path="/supervisor_thread_id"),
        )

        self.ticket_container = await self.database.create_container_if_not_exists(
            id="tickets",
            partition_key=PartitionKey(path="/id"),
        )

        # 2. FIXED: Properly initialize the checkpointer as an async context manager
        self._checkpointer_ctx = CosmosDBSaver.from_conn_info(
            endpoint=config.COSMOSDB_ENDPOINT,
            key=config.COSMOSDB_KEY,
            database_name="enterprise-ai-memory",
            container_name="checkpoints"
        )
        """
        self.checkpointer = CosmosDBSaver.from_client(
            client=self.client,
            database_name="enterprise-ai-memory",
            container_name="checkpoints"
        )
        """
        # Manually enter the checkpointer context manager to persist it inside the class
        self.checkpointer = await self._checkpointer_ctx.__aenter__()
        
        print("Checkpointer initialized successfully.")

    async def close(self):
        """Close the Azure Cosmos DB asynchronous client."""
        if self.client is not None:
            await self.client.close()
            self.client = None
            self.checkpointer = None
            print("Checkpoint client closed.")

        #Close the Azure Cosmos DB client and the checkpointer context."""
        # 1. Cleanly exit the checkpointer connection pool
        if self._checkpointer_ctx is not None:
            await self._checkpointer_ctx.__aexit__(None, None, None)
            self._checkpointer_ctx = None
            self.checkpointer = None


memory_client = CheckpointMemoryClient()
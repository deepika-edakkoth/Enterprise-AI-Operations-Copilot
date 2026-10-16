import asyncio
from contextlib import asynccontextmanager
from config.langsmith_config import configure_langsmith
from fastapi import FastAPI
from api.api import router
from memory.checkpoint_memory import memory_client
from startup.initialize_agents import initialize_agents
from agents.executors.supervisor_executor import run_supervisor as executor_run_supervisor


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Initializing memory...")
        await memory_client.initialize()

        print("Initializing agents...")
        await initialize_agents()

        configure_langsmith()
        print("Application initialized successfully.")

        yield
    finally:
        print("Shutting down...")

        await memory_client.close()

        print("Memory client closed.")

app = FastAPI(
    title="Enterprise AI Operations Copilot",
    description="An AI-powered operations copilot for enterprise IT and HR tasks.",
    lifespan=lifespan
)

app.include_router(router)

if __name__ == "__main__":

    async def test():
        try:
            await memory_client.initialize()
            await initialize_agents()
            
            result = await executor_run_supervisor(
                "How do I deploy Azure Functions?",
                "test-thread1"
            )

            print(result)
        finally:
            await memory_client.close()

    asyncio.run(test())
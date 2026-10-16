from agents import registry
from agents.builders.learning_builder import create_learning_agent
from agents.builders.hr_builder import create_hr_agent
from agents.builders.ticket_builder import create_ticket_agent
from agents.builders.it_builder import create_it_agent
from agents.builders.supervisor_builder import create_supervisor_agent
from memory.checkpoint_memory import memory_client

async def initialize_agents():

    print("Initializing agents...")

    registry.learning_agent = await create_learning_agent()

    registry.hr_agent = await create_hr_agent()

    registry.ticket_agent = await create_ticket_agent()

    registry.it_agent = await create_it_agent()

    registry.supervisor_agent = await create_supervisor_agent(
        memory_client.checkpointer
    )

    print("Agents initialized successfully.")
from langchain.tools import tool
from langchain.agents import create_agent
from services.model_client import FoundryModelClient
from prompts.ticket_prompt import TICKET_PROMPT

async def create_ticket_agent():
    # Initialize model client
    client = FoundryModelClient()

    # Create a ticket subagent
    ticket_agent = create_agent(
            model=client.model, 
            tools=[],
            system_prompt=TICKET_PROMPT
        )

    return ticket_agent
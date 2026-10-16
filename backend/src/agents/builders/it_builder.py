from langchain.tools import tool
from langchain.agents import create_agent
from services.model_client import FoundryModelClient
from prompts.it_prompt import IT_PROMPT

async def create_it_agent():
    # Initialize model client
    client = FoundryModelClient()

    # Create a it subagent
    it_agent = create_agent(
        model=client.model, 
        tools=[],
        system_prompt=IT_PROMPT
    )
    return it_agent
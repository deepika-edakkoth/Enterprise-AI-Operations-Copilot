from langchain.tools import tool
from langchain.agents import create_agent
from services.model_client import FoundryModelClient
from prompts.hr_prompt import HR_PROMPT

async def create_hr_agent():
    # Initialize model client
    client = FoundryModelClient()

    # Create a hr subagent
    hr_agent = create_agent(
            model=client.model, 
            tools=[],
            system_prompt=HR_PROMPT
        )

    return hr_agent
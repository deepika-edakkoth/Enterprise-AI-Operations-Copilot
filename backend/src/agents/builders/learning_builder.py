from langchain.agents import create_agent
from services.model_client import FoundryModelClient
from services.learn_mcp_client import LearningMCPClient
from prompts.learning_prompt import LEARNING_PROMPT

async def create_learning_agent():
    # Initialize model client
    client = FoundryModelClient()

    #Initialize the learning mcp client
    learn_mcp = LearningMCPClient()

    await learn_mcp.initialize()

    learn_tools = learn_mcp.get_tools()

    # Create a subagent
    learning_agent = create_agent(
            model=client.model, 
            tools=learn_tools,
            system_prompt=LEARNING_PROMPT
        )

    return learning_agent
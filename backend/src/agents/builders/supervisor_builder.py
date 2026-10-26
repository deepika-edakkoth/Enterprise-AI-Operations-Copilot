from langchain.agents import create_agent
from services.model_client import FoundryModelClient
from agents.executors.learning_executor import call_learn_agent
from agents.executors.hr_executor import call_hr_agent
from agents.executors.ticket_executor import call_ticket_agent
from prompts.supervisor_prompt import SUPERVISOR_PROMPT

async def create_supervisor_agent(checkpointer):
    # Initialize model client
    model_client = FoundryModelClient()


    supervisor_agent = create_agent(
        model         =   model_client.model,
        tools         =   [call_learn_agent, call_hr_agent, call_ticket_agent],
        system_prompt =   SUPERVISOR_PROMPT,
        middleware    =   [],
        checkpointer  =   checkpointer,
    )

    return supervisor_agent
from langchain.tools import tool
from langchain.agents import create_agent
from services.model_client import FoundryModelClient
from prompts.ticket_prompt import TICKET_PROMPT
from tools.ticket_tools import build_ticket_tools
from services.ticket_store import get_ticket_store
from langchain.agents.middleware import HumanInTheLoopMiddleware
from memory.checkpoint_memory import memory_client
from services.ticket_context import TicketContext

async def create_ticket_agent():
    # Initialize model client
    client = FoundryModelClient()
    store = get_ticket_store()
    ticket_tools = build_ticket_tools(store)

    print("Ticket tools:",
        [tool.name for tool in ticket_tools]
    )

    # Create a ticket subagent
    ticket_agent        =   create_agent(
            model       =   client.model, 
            tools       =   ticket_tools,
            system_prompt=  TICKET_PROMPT,
            middleware  =   [ 
                HumanInTheLoopMiddleware(
                    interrupt_on={
                        "activate_ticket": {
                            "allowed_decisions": ["approve", "reject"],
                            "description": (
                                "Review this ticket before activating it."
                            ),
                        },
                        "create_ticket_draft": False,
                    },
                    description_prefix="Ticket approval required",
                ) 
            ], 
            checkpointer =   memory_client.checkpointer,
            context_schema=  TicketContext
        )
    return ticket_agent
from langchain_core.messages import HumanMessage
from agents import registry

async def run_supervisor(
    user_query: str,
    thread_id: str
):
    supervisor_agent = registry.supervisor_agent

    if supervisor_agent is None:
        raise RuntimeError(
            "Supervisor agent is not initialized. "
        )

    print(f"Running supervisor agent with query: {user_query} and thread_id: {thread_id}")
    
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    response = await supervisor_agent.ainvoke(
        {
            "messages": [
                HumanMessage(content=user_query)
            ]
        },
        config=config
    )

    for msg in response["messages"]:
        msg.pretty_print()

    final_response = response["messages"][-1].content

    print (f"Supervisor agent final response: {final_response}")

    return final_response
from langchain.tools import tool,ToolRuntime
from langsmith import traceable
from agents import registry
import traceback
from services.conversation_service import (
    ConversationService
)

# Wrap it as an async tool so it stays in the async execution path
@tool(description="Use this tool to call the Ticket Agent for creating, retrieving, and updating IT support tickets.")
@traceable
async def call_ticket_agent(
    query: str, 
    runtime: ToolRuntime):
    try:
        print (f"Calling Ticket Agent with query: {query}")
        # Get the supervisor thread ID from the running workflow.
        supervisor_thread_id = runtime.config["configurable"]["thread_id"]

        print(f"Supervisor Agent thread ID runtime:", {supervisor_thread_id})

        ticket_thread_id = (
            ConversationService.create_conversation()
        )

        config = {
                "configurable": {
                    "thread_id": ticket_thread_id
                }
            }

        result = await registry.ticket_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user", 
                        "content": query
                    }
                ]
            },
            config=config,
            context={
                "supervisor_thread_id": supervisor_thread_id,
                "ticket_thread_id": ticket_thread_id,
            },
            version="v2",
        )

        interrupts = result.interrupts or []
        if not interrupts:
            return {
                "status": "success",
                "response": result["messages"][-1].content
            }


        print("Interrupts detected. Agent execution paused for human review. Pausing execution for human review.")

        # Here you can implement logic to notify a human for review.
        for interrupt in result.interrupts:
            print(f"Interrupt value: {interrupt.value}")
            tool_name = interrupt.value["action_requests"][0]["name"]
            print(f"Interrupt from tool: {tool_name}")

            state = await registry.ticket_agent.aget_state(config)
            print("Checkpoint state:", state)
            print("Thread ID:", ticket_thread_id)
            print("Checkpoint config:", state.config)
            print("Parent config:", state.parent_config)
            print("Next nodes:", state.next)
            print("Tasks:", state.tasks)
            for task in state.tasks:
                print("TASK:", task)
                print("INTERRUPTS:", task.interrupts)

            # Inspect the exact checkpoint saved for this thread.
            history = [
                snapshot
                async for snapshot in registry.ticket_agent.aget_state_history(
                    config
                )
            ]

            print("Checkpoint history count:", len(history))

            for index, snapshot in enumerate(history[:5]):
                print(f"\nCheckpoint {index}")
                print("Config:", snapshot.config)
                print("Next:", snapshot.next)
                print("Tasks:", snapshot.tasks)
                print("Metadata:", snapshot.metadata)

            return {
                "status": "pending_approval",
                "interrupt": interrupt.value
            }            

    except Exception as e:
        print("ERROR in call_ticket_agent")
        print(type(e).__name__)
        print(str(e))
        traceback.print_exc()

        return {
            "status": "error",
            "error": str(e)
        }
from langgraph.types import Command

def create_resume_command(decision: str) -> Command:
    """Create a resume command based on the decision."""
    resume_command = None
    match decision:
            case "approved":
                resume_command = Command(
                    resume={"decisions": [{"type": "approve"}]}
                )
    
            case "rejected":
                resume_command = Command(
                    resume={"decisions": [{"type": "reject"}]}
                )

            case _:
                raise ValueError(
                    f"Invalid approval decision: {decision}"
                )

    return resume_command

async def resume_ticket_agent(
    ticket_agent,
    ticket_thread_id: str,
    decision: str,
):
    """Resume an interrupted Ticket Agent execution."""

    config = {
        "configurable": {
            "thread_id": ticket_thread_id
        }
    }


    # 1. Inspect the checkpoint BEFORE resuming.
    state_before = await ticket_agent.aget_state(config)

    if not state_before.tasks or not any(
        task.interrupts for task in state_before.tasks
    ):
        return {
            "status": "no_interrupt",
            "message": "No pending approval was found for this thread."
        }

    # 2. Resume the existing interrupted execution.
    command = create_resume_command(decision)

    result = await ticket_agent.ainvoke(
        command,
        config=config,
        version="v2",
    )

    state_after = await ticket_agent.aget_state(config)

    if result.interrupts:
        return {
            "status": "pending_approval",
            "message": "The workflow is waiting for another approval."
        }

    if state_after.next:
        return {
            "status": "in_progress",
            "message": "The workflow has not finished yet."
        }
    
    return {
        "status": "completed",
        "message": f"Ticket workflow resumed with decision: {decision}."
    }

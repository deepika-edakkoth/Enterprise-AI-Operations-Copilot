from fastapi import APIRouter , Request
from fastapi import HTTPException
from pprint import pprint
from .model import (
    ChatRequest,
    ChatResponse,
    ConversationResponse,
    RejectRequest
)
from services.conversation_service import (
    ConversationService
)
from services.conversation_store import (
    get_conversation_store
)
from agents.executors.supervisor_executor import (
    run_supervisor
)
from agents import registry
from services.ticket_store import (
    get_ticket_store
)
from services.approval_payload import build_approval_payload
from services.extract_interrupt import extract_approval
from services.hitl_resume_handler import resume_ticket_agent

router = APIRouter()

@router.post("/conversation",  response_model=ConversationResponse)
async def create_conversation():

    supervisor_thread_id = (
        ConversationService.create_conversation()
    )

    store = get_conversation_store()
    await store.create(supervisor_thread_id)

    return {
        "supervisor_thread_id": supervisor_thread_id
    }

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest
):
    store = get_conversation_store()

    conversation = await store.get(request.supervisor_thread_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found. Create a new chat first.",
        )

    # Save the user's message before calling the agent.
    await store.add_message(
        request.supervisor_thread_id,
        "user",
        request.query,
    )

    try:
        ai_response = await run_supervisor(
            user_query=request.query,
            supervisor_thread_id=request.supervisor_thread_id
        )

        print("AI response received:")
        interrupt_data = await extract_approval(ai_response)
        try:
            if interrupt_data:
                print("Approval request detected")

                action_requests = interrupt_data["action_requests"]

                draft_id = action_requests[0]["args"]["id"]
                print(f"Draft Id, {draft_id}")
                ticket_store = get_ticket_store()
                #await ticket_store.update_thread_id(draft_id, request.supervisor_thread_id)
                ticket = await ticket_store.get_ticket(draft_id)
                payload = build_approval_payload(request, ticket)
                #print(f"payload sending to chat, {payload}")
                return payload
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Approval error:", str(e))
            raise

    except Exception:
        # Keep your existing error handling/logging here.
        raise HTTPException(
            status_code=500,
            detail="The AI agent failed to process the request.",
        )

    final_response =  ai_response["messages"][-1].content

    # Save the assistant response after the agent finishes.
    await store.add_message(
        request.supervisor_thread_id,
        "assistant",
        final_response,
    )

    return {
        "status": "completed",
        "supervisor_thread_id": request.supervisor_thread_id,
        "message": (
            final_response
            if final_response is not None
            else "Request completed."
        )
    }

@router.get("/conversations")
async def list_conversations():
    store = get_conversation_store()
    return await store.list_conversations()


@router.get("/conversations/{supervisor_thread_id}")
async def get_conversation(supervisor_thread_id: str):
    store = get_conversation_store()
    conversation = await store.get(supervisor_thread_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation

@router.get("/ticket/pending")
async def get_pending_tickets(request: Request):
    store = request.app.state.ticket_store
    return await store.list_tickets(status="Pending Approval")


@router.get("/tickets")
async def get_all_tickets(request: Request):
    store = request.app.state.ticket_store
    return await store.list_tickets()


@router.post("/tickets/{document_id}/approve")
async def approve_ticket(document_id: str, request: Request):

    store = request.app.state.ticket_store

    try:
        # 1. Retrieve the ticket draft from Cosmos DB.
        ticket = await store.get_ticket(document_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket draft not found.",
            )

        # Check whether a ticket for this conversation
        # has already been approved.
        if ticket.get("status") == "Approved":
            return {
                "status": "already_approved",
                "message": "This ticket is already approved.",
                "ticket_id" : ticket.get("ticket_id")
            }

        # 2. Get the original conversation's thread ID.
        ticket_thread_id = ticket.get("ticket_thread_id")

        print(f"Ticket Thread id, {ticket_thread_id}")
        if not ticket_thread_id:
            raise HTTPException(
                status_code=400,
                detail="Thread ID is missing from the ticket.",
            )
        try:
            # 3. Resume the interrupted Ticket Agent using
            #    the ticket thread ID.
            result = await resume_ticket_agent(
                ticket_agent        =   registry.ticket_agent,
                ticket_thread_id    =   ticket_thread_id,
                decision            =   "approved",
            )

            ticket = await store.get_ticket(document_id)
            ticket_id = ticket.get("ticket_id")
            result["ticket_id"] = ticket_id
            result["message"] = f"Ticket is generated with Id {ticket_id}"
            # Save the assistant response after the agent finishes.
            conversation_store = get_conversation_store()
            await conversation_store.add_message(
                ticket.get("supervisor_thread_id"),
                "assistant",
                result["message"],
            )
            
            return result
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Approval error:", str(e))
            raise

    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Unable to approve ticket",
        ) from exc


@router.post("/tickets/{document_id}/reject")
async def reject_ticket(
    document_id: str,
    request: Request,
    body: RejectRequest,
):
    store = request.app.state.ticket_store
    
    try:
        # 1. Retrieve the ticket draft from Cosmos DB.
        ticket = await store.get_ticket(document_id)

        if not ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket draft not found.",
            )

        # Check whether a ticket for this conversation
        # has already been approved.
        if ticket.get("status") == "Rejected":
            return {
                "status": "already_rejected",
                "message": "This ticket is already approved.",
            }

        # 2. Get the original conversation's thread ID.
        ticket_thread_id = ticket.get("ticket_thread_id")

        if not ticket_thread_id:
            raise HTTPException(
                status_code=400,
                detail="Thread ID is missing from the ticket.",
            )

        # 3. Resume the interrupted Ticket Agent using
        #    the original thread ID.
        result = await resume_ticket_agent(
            ticket_agent=registry.ticket_agent,
            ticket_thread_id=ticket_thread_id,
            decision="rejected",
        )

        ticket = await store.reject_ticket(
            document_id,
            reason=body.reason,
        )
        return result

    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except Exception as exc:
        # Log the real exception in production.
        raise HTTPException(
            status_code=500,
            detail="Unable to approve ticket",
        ) from exc

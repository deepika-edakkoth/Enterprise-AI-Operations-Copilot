from fastapi import APIRouter

from .model import (
    ChatRequest,
    ChatResponse,
    ConversationResponse
)
from services.conversation_service import (
    ConversationService
)
from agents.executors.supervisor_executor import (
    run_supervisor
)

router = APIRouter()

@router.post("/conversation",  response_model=ConversationResponse)
async def create_conversation():

    thread_id = (
        ConversationService.create_conversation()
    )

    return {
        "thread_id": thread_id
    }

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest
):

    response = await run_supervisor(
        user_query=request.query,
        thread_id=request.thread_id
    )

    return {
        "ai_response": response
    }
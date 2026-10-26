from pydantic import BaseModel

class ChatRequest(BaseModel):
    supervisor_thread_id: str
    query: str

class ChatResponse(BaseModel):
    status: str
    supervisor_thread_id: str
    ticket: dict | None = None
    message: str

class ConversationResponse(BaseModel):
    supervisor_thread_id: str

class RejectRequest(BaseModel):
    reason: str = ""

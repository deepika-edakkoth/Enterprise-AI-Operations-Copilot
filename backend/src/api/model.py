from pydantic import BaseModel

class ChatRequest(BaseModel):
    thread_id: str
    query: str

class ChatResponse(BaseModel):
    ai_response: str


class ConversationResponse(BaseModel):
    thread_id: str
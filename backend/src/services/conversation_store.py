
from datetime import datetime, timezone
from fastapi import HTTPException
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from memory.checkpoint_memory import memory_client


class ConversationStore:
    def __init__(self, container):
        self.container = container

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat()

    async def create(self, supervisor_thread_id: str):
        now = self.now()

        document = {
            "id": supervisor_thread_id,
            "supervisor_thread_id": supervisor_thread_id,
            "title": "New chat",
            "messages": [],
            "created_at": now,
            "updated_at": now,
        }

        await self.container.create_item(body=document)
        return document

    async def list_conversations(self):
        query = """
            SELECT TOP 5 c.id, c.supervisor_thread_id, c.title,
                   c.created_at, c.updated_at
            FROM c
            ORDER BY c.updated_at DESC
        """

        results = []
        async for item in self.container.query_items(
            query=query,
        ):
            results.append(item)

        return results

    async def get(self, thread_id: str):
        try:
            return await self.container.read_item(
                item=thread_id,
                partition_key=thread_id,
            )
        except CosmosResourceNotFoundError:
            return None

    async def add_message(
        self,
        supervisor_thread_id: str,
        role: str,
        content: str,
    ):
        conversation = await self.get(supervisor_thread_id)
        
        if conversation is None:
            return None

        if role not in ("user", "assistant"):
            raise ValueError("Unsupported message role")

        conversation["messages"].append({
            "role": role,
            "content": content,
            "created_at": self.now(),
        })

        # Use the first user message as the conversation title.
        if role == "user" and conversation["title"] == "New chat":
            conversation["title"] = content[:60]

        conversation["updated_at"] = self.now()

        await self.container.replace_item(
            item=supervisor_thread_id,
            body=conversation,
        )

        return conversation

    
def get_conversation_store():
    container = getattr(
        memory_client,
        "conversations_container",
        None,
    )

    if container is None:
        raise HTTPException(
            status_code=503,
            detail="Conversation storage is not initialized.",
        )

    return ConversationStore(container)


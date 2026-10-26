from datetime import datetime, timezone
from uuid import uuid4
from fastapi import HTTPException
from memory.checkpoint_memory import memory_client



class TicketStore:
    def __init__(self, container):
        self.container = container

    async def close(self):
        if self.client is not None:
            await self.client.close()

    async def create_draft(
        self,
        title: str,
        description: str,
        priority: str,
        category: str,
        supervisor_thread_id: str,
        ticket_thread_id: str
    ) -> dict:
        ticket = {
            "id": str(uuid4()),
            "supervisor_thread_id": supervisor_thread_id,
            "ticket_thread_id": ticket_thread_id,
            "ticket_id": None, # Permanent ID not assigned yet
            "title": title,
            "description": description,
            "priority": priority,
            "category": category,
            "status": "Pending Approval",
            "approval_status": "Pending",
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        return await self.container.create_item(body=ticket)

    async def update_thread_id(
        self,
        draft_id: str,
        supervisor_thread_id: str,
    ) -> dict:
        ticket = await self.container.read_item(
            item=draft_id,
            partition_key=draft_id,
        )

        ticket["supervisor_thread_id"] = supervisor_thread_id

        return await self.container.replace_item(
            item=draft_id,
            body=ticket,
        )

    async def list_pending_by_thread(
        self,
        supervisor_thread_id: str,
    ) -> list[dict]:
        query = """
            SELECT * FROM c
            WHERE c.supervisor_thread_id = @supervisor_thread_id
            AND c.approval_status = @approval_status
        """

        parameters = [
            {"name": "@supervisor_thread_id", "value": supervisor_thread_id},
            {"name": "@approval_status", "value": "Pending"},
        ]

        items = []
        async for item in self.container.query_items(
            query=query,
            parameters=parameters,
        ):
            items.append(item)

        return items


    async def get_ticket(self, id: str) -> dict | None:
        try:
            return await self.container.read_item(
                item=id,
                partition_key=id,
            )
        except Exception:
            return None
       

    async def list_tickets(
        self,
        status: str | None = None,
    ) -> list[dict]:
        if status:
            query = """
                SELECT * FROM c
                WHERE c.status = @status
                ORDER BY c.created_at DESC
            """
            parameters = [
                {"name": "@status", "value": status}
            ]
        else:
            query = """
                SELECT * FROM c
                ORDER BY c.created_at DESC
            """
            parameters = []

        results = self.container.query_items(
            query=query,
            parameters=parameters,
        )

        tickets = []
        async for item in results:
            tickets.append(item)

        return tickets

    async def approve_ticket(self, document_id: str) -> dict:
        ticket = await self.container.read_item(
            item=document_id,
            partition_key=document_id,
        )

        if ticket["approval_status"] != "Pending":
            raise ValueError("This draft is no longer pending.")

        ticket["ticket_id"] = (
            f"TKT-{ticket['id'][:8].upper()}"
        )
        ticket["status"] = "Open"
        ticket["approval_status"] = "Approved"
        ticket["approved_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        return await self.container.replace_item(
            item=document_id,
            body=ticket,
        )

    async def reject_ticket(
        self,
        document_id: str,
        reason: str = "",
    ) -> dict:
        ticket = await self.container.read_item(
            item=document_id,
            partition_key=document_id,
        )

        if ticket["approval_status"] != "Pending":
            raise ValueError("This draft is no longer pending.")

        ticket["status"] = "Rejected"
        ticket["approval_status"] = "Rejected"
        ticket["rejection_reason"] = reason
        ticket["rejected_at"] = datetime.now(
            timezone.utc
        ).isoformat()

        return await self.container.replace_item(
            item=document_id,
            body=ticket,
        )

def get_ticket_store():
    container = getattr(
        memory_client,
        "ticket_container",
        None,
    )

    if container is None:
        raise HTTPException(
            status_code=503,
            detail="Ticket storage is not initialized.",
        )

    return TicketStore(container)
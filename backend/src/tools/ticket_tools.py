from langchain.tools import tool
from services.ticket_store import TicketStore
from langchain.tools import tool, ToolRuntime
from services.ticket_context import TicketContext

def build_ticket_tools(ticket_store: TicketStore):

    @tool
    async def create_ticket_draft(
        title: str,
        description: str,
        runtime: ToolRuntime[TicketContext],  
        priority: str = "Medium",
        category: str = "IT Support",    
    ) -> dict:
        """Create a ticket draft immediately.

        Infer the title and description from the user's request.
        Use Medium priority and IT Support category when unspecified.
        Do not ask the user for optional fields.
        """

        print("Create ticket draft tool called...")
        if priority not in {"Low", "Medium", "High"}:
            return {"error": "Invalid priority."}

        supervisor_thread_id = runtime.context["supervisor_thread_id"]
        ticket_thread_id = runtime.context["ticket_thread_id"]

        print("Supervisor thread:", supervisor_thread_id)
        print("Ticket thread:", ticket_thread_id)
        
        return await ticket_store.create_draft(
            title=title,
            description=description,
            priority=priority,
            category=category,
            supervisor_thread_id=supervisor_thread_id,
            ticket_thread_id=ticket_thread_id,
        )

    @tool
    async def activate_ticket(id: str) -> dict:
        """Request activation of an existing pending ticket draft.

        This tool is protected by HumanInTheLoopMiddleware.
        Only after human approval may it generate the permanent ticket ID
        and change the ticket status to Open.
        Pass the internal ID returned by create_ticket_draft.
        """
        ticket = await ticket_store.get_ticket(id)
        
        print("Activate ticket tool called...")
        if not ticket:
            raise ValueError("Ticket not found")

        if ticket["approval_status"] != "Pending":
            raise ValueError("Ticket is no longer pending approval")

        return await ticket_store.approve_ticket(ticket["id"])

    @tool
    async def get_ticket(ticket_id: str) -> dict:
        """Retrieve a ticket using its document ID or ticket number."""

        ticket = await ticket_store.get_ticket(ticket_id)

        if ticket is None:
            return {"error": "Ticket not found."}

        return ticket

    @tool
    async def list_tickets(status: str = "") -> list[dict]:
        """List tickets. Optional status: Pending Approval,
        Open, or Rejected. Leave empty to list all tickets.
        """

        allowed = {"Pending Approval", "Open", "Rejected"}

        if status and status not in allowed:
            return {"error": "Invalid ticket status."}

        return await ticket_store.list_tickets(
            status=status or None
        )

    return [
        create_ticket_draft,
        get_ticket,
        list_tickets,
        activate_ticket,
    ]
from typing import TypedDict

class TicketContext(TypedDict):
    supervisor_thread_id: str
    ticket_thread_id: str

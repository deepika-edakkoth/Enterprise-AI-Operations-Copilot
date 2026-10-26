def build_approval_payload(request, ticket):
    return {
        "status": "pending_approval",
        "supervisor_thread_id": request.supervisor_thread_id,
        "ticket": {
            "ticket_draft_id": ticket["id"],
            "supervisor_thread_id": ticket["supervisor_thread_id"],
            "ticket_thread_id": ticket["ticket_thread_id"],
            "title": ticket["title"],
            "description": ticket["description"],
            "priority": ticket["priority"],
            "category": ticket["category"],
            "status": ticket["status"],
        },
        "message": "Please review this ticket before activation.",
    }
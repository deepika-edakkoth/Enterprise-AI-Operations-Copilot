
import streamlit as st
import config
import requests

def resolve_approval_card(
    ticket_draft_id: str,
    decision: str,
    api_result: dict,
) -> None:
    """Hide a resolved approval card and show the API result."""

    # Hide only the card belonging to this ticket.
    for msg in st.session_state.messages:
        if (
            msg.get("role") == "approval"
            and msg.get("ticket_draft_id") == ticket_draft_id
        ):
            msg["resolved"] = True
            msg["decision"] = decision
            break

    # Add a normal chat message with the API response.
    ticket_id = api_result.get("ticket_id")
    status = api_result.get("status", "unknown")
    message = api_result.get(
        "message",
        f"Ticket {decision} response received. Ticket Id is {ticket_id}",
    )

    st.session_state.messages.append({
        "role": "approval",
        "content": message,
        "ticket_draft_id": ticket_draft_id,
        "approval_status": status,
    })

def handle_decision(ticket_draft_id: str, decision: str):
    action = "approve" if decision == "approved" else "reject"
    # Show progress in the chat while the API request runs.
    with st.chat_message("assistant"):
        with st.spinner(
            "Approving ticket..." if decision == "approved"
            else "Rejecting ticket..."
        ):
            try:
                response = requests.post(
                    f"{config.API_BASE_URL}/tickets/{ticket_draft_id}/{action}",
                    timeout=30,
                )
                response.raise_for_status()
                api_result = response.json()

                status = api_result.get("status", "").lower()
                # Only resolve the card when the API confirms the outcome.
                if status in {
                    "completed",
                    "approved",
                    "rejected",
                    "success",
                }:
                    resolve_approval_card(
                        ticket_draft_id=ticket_draft_id,
                        decision=decision,
                        api_result=api_result,
                    )
                    st.rerun()

                elif status in {"pending_approval", "in_progress"}:
                    st.warning(
                        api_result.get(
                            "message",
                            "The ticket workflow is still processing.",
                        )
                    )
                else:
                    st.warning(
                        api_result.get(
                            "message",
                            "The ticket decision has not been completed.",
                        )
                    )

            except requests.RequestException as exc:
                st.error(f"Failed to process ticket decision: {exc}")
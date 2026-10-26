import requests
import streamlit as st
from utilities.chat_helpers import handle_decision

def render_approval_card(payload: dict):
    ticket = payload["ticket"]
    ticket_draft_id = ticket["ticket_draft_id"]

    with st.container(border=True):
        st.subheader("Review ticket draft")
        st.write(f"**Title:** {ticket['title']}")
        st.write(f"**Description:** {ticket['description']}")
        st.write(f"**Priority:** {ticket['priority']}")
        st.write(f"**Category:** {ticket['category']}")
        st.caption("Status: Pending Approval")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Approve",
                key=f"approve_{ticket_draft_id}",
                type="primary",
            ):
                handle_decision(ticket_draft_id, "approved")

        with col2:
            if st.button(
                "Reject",
                key=f"reject_{ticket_draft_id}",
            ):
                handle_decision(ticket_draft_id, "rejected")
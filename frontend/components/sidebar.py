
import requests
import streamlit as st

import config


def render_sidebar():
    st.sidebar.title("Enterprise AI")

    if st.sidebar.button("＋ New Chat", use_container_width=True):
        st.session_state.pop("supervisor_thread_id", None)
        st.session_state.pop("pending_approval", None)
        st.session_state.messages = []
        st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Previous Chats")

    try:
        response = requests.get(
            f"{config.API_BASE_URL}/conversations",
            timeout=15,
        )
        response.raise_for_status()
        conversations = response.json()

    except requests.RequestException as exc:
        st.sidebar.error(f"Could not load chats: {exc}")
        conversations = []

    if not conversations:
        st.sidebar.caption("No previous chats yet.")

    for conversation in conversations:
        supervisor_thread_id = conversation["supervisor_thread_id"]
        title = conversation.get("title") or "New chat"

        # Streamlit button keys must be unique.
        if st.sidebar.button(
            title,
            key=f"chat_{supervisor_thread_id}",
            use_container_width=True,
        ):
            try:
                response = requests.get(
                    f"{config.API_BASE_URL}/conversations/{supervisor_thread_id}",
                    timeout=15,
                )
                response.raise_for_status()
                data = response.json()

                st.session_state.supervisor_thread_id = supervisor_thread_id
                st.session_state.messages = [
                    {
                        "role": msg["role"],
                        "content": msg["content"],
                    }
                    for msg in data.get("messages", [])
                ]
                # Clear any approval from the previously opened conversation
                st.session_state.pop("pending_approval", None)
                st.rerun()

            except requests.RequestException as exc:
                st.sidebar.error(f"Could not open chat: {exc}")

    st.sidebar.divider()

    if st.sidebar.button("Traces", use_container_width=True):
        st.session_state.page = "traces"
        st.rerun()

    if st.sidebar.button("Clear Current Chat", use_container_width=True):
        st.session_state.pop("supervisor_thread_id", None)
        st.session_state.pop("pending_approval", None)
        st.session_state.messages = []
        st.rerun()
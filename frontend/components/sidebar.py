import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.title("Enterprise AI")
        st.caption("Operations Copilot")

        # Primary action
        if st.button(
            "＋ New AI Chat",
            use_container_width=True,
        ):
            st.session_state.active_view = "chat"
            st.session_state.messages = []
            st.session_state.current_chat_id = None
            st.rerun()

        st.divider()

         # Navigation
        st.caption("WORKSPACE")

        if st.button("◉ Traces", use_container_width=True):
            st.session_state.active_view = "traces"
            st.rerun()

        st.divider()

        # Previous conversations
        st.caption("PREVIOUS CHATS")

        # Example placeholder until chat history is implemented
        st.caption("Your saved conversations will appear here.")

        st.divider()

        # Chat management
        if st.button(
            "Clear current chat",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.rerun()

        st.divider()
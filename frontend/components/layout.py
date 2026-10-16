import streamlit as st

from .sidebar import render_sidebar
from ui.chat import render_chat
from ui.traces import render_traces

def render_page():

    st.set_page_config(
        page_title="Enterprise AI Operations Copilot",
        layout="wide"
    )

    if "active_view" not in st.session_state:
        st.session_state.active_view = "chat"

    render_sidebar()

    if st.session_state.active_view == "traces":
        render_traces()
    else:
        render_chat()
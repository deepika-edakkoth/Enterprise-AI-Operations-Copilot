import streamlit as st
import requests
import config
from ui.style_loader import load_css

def render_chat():

    load_css("chat.css")

    st.title(
        "Enterprise AI Operations Copilot"
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-row user-row">'
                f'<div class="user-bubble">'
                f'{msg["content"]}'
                f'</div></div>',
                unsafe_allow_html=True
            )

        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    prompt = st.chat_input(
        "Ask a question..."
    )

    if prompt:

        # Create a conversation(thread id) only once per chat session
        if "thread_id" not in st.session_state:
            try:
                chat_id_response = requests.post(
                    f"{config.API_BASE_URL}conversation",
                    timeout=30
                )

                chat_id_response.raise_for_status()
                
                data = chat_id_response.json()
                thread_id = data["thread_id"]
                st.session_state.thread_id = thread_id

            except requests.RequestException as e:
                st.error(f"Could not create conversation: {e}")
                return

        # Save and display the user's message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # Display user message on the right
        st.markdown(
            f'<div class="chat-row user-row">'
            f'<div class="user-bubble">'
            f'{prompt}'
            f'</div></div>',
            unsafe_allow_html=True
        )

        # Call backend agent
        try:
            with st.spinner("AI agent is thinking..."):
                response = requests.post(
                    f"{config.API_BASE_URL}chat",
                    json={
                        "query": prompt,
                        "thread_id": st.session_state.thread_id
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()
                answer = data["ai_response"]
                #answer = response.json()["ai_response"]

            # IMPORTANT: Save the assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            # Refresh to render both messages from chat history
            st.rerun()

        except requests.RequestException as e:
            st.error(f"Backend request failed: {e}")

        except (ValueError, KeyError) as e:
            st.error(f"Invalid response from backend: {e}")
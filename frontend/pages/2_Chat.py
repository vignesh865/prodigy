import time

import streamlit as st

from query_system.service.streamlit_service import StreamlitService

st.title("Prodigy")

if not StreamlitService.should_authenticate(st):
    authentication = st.session_state["authentication"]
    # Initialize chat history
    if "messages" not in st.session_state.keys():
        st.session_state['messages'] = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display chat messages from history on app rerun
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            assistant_response = StreamlitService.get_answers(authentication.get("token"), prompt)

            # Simulate stream of response with milliseconds delay
            for sentence in assistant_response.split("\n"):
                for chunk in sentence.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                full_response += "\n"

            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.error("Not Authenticated")

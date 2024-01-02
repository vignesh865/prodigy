import json

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from query_system.service.streamlit_service import StreamlitService, LoginError

# Create an empty container
placeholder = st.empty()

if StreamlitService.should_authenticate(st):
    # Insert a form in the container
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if email and password:
            try:
                response = StreamlitService.call_login(email, password, email)
                st.session_state["authentication"] = response
                # placeholder.empty()
                st.success("Login successful")
                switch_page("Chat")
            except LoginError as error:
                message = json.loads(str(error)).get("detail")
                st.error(f"Login failed - {error}")
            except ValueError as error:
                st.error(f"Login failed - {error}")
else:
    switch_page("Chat")

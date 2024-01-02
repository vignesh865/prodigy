from http import HTTPStatus

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_javascript import st_javascript

from query_system.service.streamlit_service import StreamlitService, LoginError

st.set_page_config(
    page_icon="👋",
    layout="wide"
)

google_image_path = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGZpbGw9IiNGRkMxMDciIGQ9Ik00My42MTEsMjAuMDgzSDQyVjIwSDI0djhoMTEuMzAzYy0xLjY0OSw0LjY1Ny02LjA4LDgtMTEuMzAzLDhjLTYuNjI3LDAtMTItNS4zNzMtMTItMTJjMC02LjYyNyw1LjM3My0xMiwxMi0xMmMzLjA1OSwwLDUuODQyLDEuMTU0LDcuOTYxLDMuMDM5bDUuNjU3LTUuNjU3QzM0LjA0Niw2LjA1MywyOS4yNjgsNCwyNCw0QzEyLjk1NSw0LDQsMTIuOTU1LDQsMjRjMCwxMS4wNDUsOC45NTUsMjAsMjAsMjBjMTEuMDQ1LDAsMjAtOC45NTUsMjAtMjBDNDQsMjIuNjU5LDQzLjg2MiwyMS4zNSw0My42MTEsMjAuMDgzeiI+PC9wYXRoPjxwYXRoIGZpbGw9IiNGRjNEMDAiIGQ9Ik02LjMwNiwxNC42OTFsNi41NzEsNC44MTlDMTQuNjU1LDE1LjEwOCwxOC45NjEsMTIsMjQsMTJjMy4wNTksMCw1Ljg0MiwxLjE1NCw3Ljk2MSwzLjAzOWw1LjY1Ny01LjY1N0MzNC4wNDYsNi4wNTMsMjkuMjY4LDQsMjQsNEMxNi4zMTgsNCw5LjY1Niw4LjMzNyw2LjMwNiwxNC42OTF6Ij48L3BhdGg+PHBhdGggZmlsbD0iIzRDQUY1MCIgZD0iTTI0LDQ0YzUuMTY2LDAsOS44Ni0xLjk3NywxMy40MDktNS4xOTJsLTYuMTktNS4yMzhDMjkuMjExLDM1LjA5MSwyNi43MTUsMzYsMjQsMzZjLTUuMjAyLDAtOS42MTktMy4zMTctMTEuMjgzLTcuOTQ2bC02LjUyMiw1LjAyNUM5LjUwNSwzOS41NTYsMTYuMjI3LDQ0LDI0LDQ0eiI+PC9wYXRoPjxwYXRoIGZpbGw9IiMxOTc2RDIiIGQ9Ik00My42MTEsMjAuMDgzSDQyVjIwSDI0djhoMTEuMzAzYy0wLjc5MiwyLjIzNy0yLjIzMSw0LjE2Ni00LjA4Nyw1LjU3MWMwLjAwMS0wLjAwMSwwLjAwMi0wLjAwMSwwLjAwMy0wLjAwMmw2LjE5LDUuMjM4QzM2Ljk3MSwzOS4yMDUsNDQsMzQsNDQsMjRDNDQsMjIuNjU5LDQzLjg2MiwyMS4zNSw0My42MTEsMjAuMDgzeiI+PC9wYXRoPgo8L3N2Zz4="


def create_integrate_button(image_path, integrate_button_text, status_button_text):
    col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.2, 0.3], gap="small")
    with col1:
        st.image(image_path, width=38)
    with col2:
        integrate_button = st.button(integrate_button_text, key="integrate")
    with col3:
        status_button = st.button(status_button_text, key="status")

    return integrate_button, status_button, col4


def nav_to(url):
    js = f'window.open("{url}", "_blank").then(r => window.parent.location.href);'
    st_javascript(js)


def manage_integrations(placeholder):
    placeholder.empty()
    st.markdown("#### Configure Integrations")

    integrate_button, status_button, status_text_col = create_integrate_button(google_image_path,
                                                                               "Sign in with Google",
                                                                               "Check Status")

    if integrate_button:
        integration_response = StreamlitService.call_google_integration(st)
        if integration_response.get("code") == HTTPStatus.TEMPORARY_REDIRECT:
            message = integration_response.get("message")
            nav_to(message.get("authorization_url"))
        else:
            message = integration_response.get("message")
            status_text_col.success(message)

    if status_button:
        is_integrated = StreamlitService.call_get_google_integration_status(st)
        if is_integrated:
            status_text_col.success("Connected with Google")
        else:
            status_text_col.error(
                "Not Integrated. Make sure you have completed the Authorization popup-ed in the other window")


def main():
    # Create an empty container
    placeholder = st.empty()

    if not StreamlitService.should_authenticate(st):
        manage_integrations(placeholder)
        return

    login, sign_up = st.tabs(["Login", "Sign Up"])

    # Insert a form in the container
    with placeholder.form("login"):
        login.markdown("#### Enter your credentials")

        email = login.text_input("Email")
        password = login.text_input("Password", type="password")
        if login.button("Login"):

            if email and password:
                try:
                    response = StreamlitService.call_login(email, password, email)
                    st.session_state["authentication"] = response
                    login.success("Login successful")
                    switch_page("Chat")
                except LoginError as error:
                    login.error(f"Login failed - {error}")
                except ValueError as error:
                    login.error(f"Login failed - {error}")

    # Insert a form in the container
    with placeholder.form("sign_up"):
        sign_up.markdown("#### Enter your credentials")

        sign_up_email = sign_up.text_input("Email", key="sign_up_email")
        sign_up_password = sign_up.text_input("Password", type="password", key="sign_up_password")
        sign_up_confirm_password = sign_up.text_input("Confirm Password", type="password",
                                                      key="sign_up_confirm_password")
        if sign_up.button("Sign up"):

            if sign_up_password != sign_up_confirm_password:
                sign_up.error(f"Password doesn't match")
                return

            if sign_up_email and sign_up_password:
                try:
                    response = StreamlitService.call_signup(sign_up_email, sign_up_password, sign_up_email)
                    st.session_state["authentication"] = response
                    sign_up.success("Sign up successful")
                    switch_page("Chat")
                except LoginError as error:
                    sign_up.error(f"Sign up failed - {error}")
                except ValueError as error:
                    sign_up.error(f"Sign up failed - {error}")
            else:
                sign_up.error(f"Invalid Email or Password")
                return


main()

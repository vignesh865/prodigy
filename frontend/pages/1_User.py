import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from query_system.service.streamlit_service import StreamlitService, LoginError


def main():
    # Create an empty container
    placeholder = st.empty()

    if not StreamlitService.should_authenticate(st):
        placeholder.empty()
        st.markdown("#### Configure Integrations")
        st.markdown("Yet to built...")
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

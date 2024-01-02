import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.session_state.pop("authentication")
switch_page("User")

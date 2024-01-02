import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from query_system.service.streamlit_service import StreamlitService

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
css = '''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)


def login_button():
    switch_page("User")


def chat_button():
    switch_page("Chat")


st.write("# Welcome to Prodigy! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Prodigy is an AI-powered knowledge management platform 
    utilizing Large Language Models (LLMs) and the Retrieval-Augmented Generation (RAG) technique 
    for Q&A systems, integrating connected pipelines with Google Drive and Kafka for data ingestion.
    Additional implementations for data ingestion can be seamlessly added with minimal effort given data pipeline in place. 
    
    **👈 Go to the Chat Page If Logged in from the sidebar** to see some examples
    of what Prodigy can do!
    ### Want to check code?
    - Check out [Prodigy](https://github.com/vignesh865/prodigy)
    - Video [Youtube](https://youtu.be/lSe6nAqhQ1A)

"""
)

st.video("https://youtu.be/lSe6nAqhQ1A", start_time=0)

if StreamlitService.should_authenticate(st):
    # st.button('Login', on_click=login_button)
    if st.button('Login'):
        switch_page("User")
else:
    # st.button('Go to chat', on_click=chat_button)
    if st.button('Go to chat'):
        switch_page("Chat")

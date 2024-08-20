import streamlit as st
from streamlit_chat import message as chat_msg
from google.cloud import dialogflow_v2 as dialogflow

from langchain_core.messages import AIMessage, HumanMessage

import uuid

import os
from dotenv import load_dotenv

load_dotenv()

# Set the path to the JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_dialogflow_api_key.json"

def init_dialogflow_session(project_id, session_id, text, language_code='en'):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        return response.query_result.fulfillment_text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(
    page_title="Bakery Receptionist",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Bakery Receptionist")

language_code = "en"
project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
session_id = str(uuid.uuid4())
print(f"session_id: {session_id}")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am the Bakery Receptionist. How can I help you?")
    ]
    
user_input = st.chat_input("Enter your message here...")

if user_input is not None and user_input.strip() != "":
    with st.spinner("Thinking..."):
        response = init_dialogflow_session(project_id, session_id, user_input, language_code)
    
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=response))
    
for i, msg in enumerate(st.session_state.chat_history):
            if i % 2 != 0:
                chat_msg(msg.content, is_user=True, key=str(i)+'_usr')
            else:
                chat_msg(msg.content, is_user=False, key=str(i)+'_ai')

        




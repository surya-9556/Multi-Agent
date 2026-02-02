import streamlit as st
import requests

from app.config.setting import Settings
from app.common import logger, CustomExceptions

logger = logger.get_logger(__name__)
c_exceptions = CustomExceptions.CustomException
settings = Settings()


st.set_page_config(page_title="Multi AI Agent",layout='centered')
st.title("Multi Agent application...!!!")

system_prompt = st.text_area("Define your AI Agent",height=20)
selected_model = st.selectbox('select your ai model..',settings.ALLOWED_MODELS)
allow_web_search = st.checkbox("Allow web search")

user_query = st.text_area("Enter your query: ", height=200)

API_URL = "http://127.0.0.1:8080/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "model_name":selected_model,
        "messages":[user_query],
        "allow_search":allow_web_search,
        "system_prompt":system_prompt,
    }

    try:
        logger.info("Sending request from api....!!")
        print(payload)

        resp = requests.post(API_URL,json=payload)
        
        if resp.status_code == 200:
            agent_resp = resp.json().get('response','')
            logger.info("Successfully recieved response from backend...")

            st.subheader("Agent Response")
            st.markdown(agent_resp.replace("\n","<br>"))
        else:

            logger.error("Backend error")
            st.error("Error with backend")

    except Exception as e:
        error_message = c_exceptions("Error occured while working with the backend", e)
        logger.error(str(error_message))
        None
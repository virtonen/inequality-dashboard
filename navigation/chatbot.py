from openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
import streamlit as st

def show_chatbot():

    with st.sidebar:
        with st.form(key="api_key_form"):
            openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
            confirm_key = st.form_submit_button("Confirm")
        if confirm_key and openai_api_key:
            st.success("API key inserted!")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    st.title("💬 Inequality Chatbot")

    st.caption("🚀 A chatbot powered by OpenAI")

    st.write("Ask me about world inequality!")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you understand global inequality better?"},
            {"role": "user", "content": "What is global inequality?"},
            {"role": "assistant", "content": "Global inequality refers to the unequal distribution of resources and opportunities among people in different countries and regions. It encompasses disparities in income, wealth, education, healthcare, and living standards."},
            {"role": "user", "content": "What are the main causes of global inequality?"},
            {"role": "assistant", "content": "The main causes of global inequality include historical colonization, economic policies, access to education, healthcare disparities, and technological advancements. Other factors such as political instability and corruption also play a significant role."},
            {"role": "user", "content": "How can global inequality be reduced?"},
            {"role": "assistant", "content": "Reducing global inequality requires a complex approach, including fair trade practices, investment in education and healthcare, progressive taxation, and international cooperation to address systemic issues. Empowering marginalized communities and ensuring equal opportunities for all are also crucial steps."}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

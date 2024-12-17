from openai import OpenAI

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


    st.title("💬 Chatbot")

    st.caption("🚀 A chatbot powered by OpenAI")

    st.write("Ask me about world inequality!")

    if "messages" not in st.session_state:

        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]



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
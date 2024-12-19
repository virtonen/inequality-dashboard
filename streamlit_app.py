import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path
from navigation.about import about
from navigation.interactive_data import show_Interactive_Data
from navigation.chatbot import show_chatbot  # Import the chatbot function

# Set the page configuration
st.set_page_config(
    page_title="World Inequality Dashboard",
    page_icon=":earth_americas:",
)

# Title at the top of the app
st.markdown(
    "<h1 style='text-align: center;'>🌎 World Inequality Dashboard</h1>", 
    unsafe_allow_html=True
)

# Navigation buttons with unique keys
def show_navigation_buttons():
    col1, col2, col3 = st.columns(3)  # Add a third column for the new button
    if col1.button("🔍 About", key="about_btn"):
        st.session_state.page = "About"
    if col2.button("📊 Interactive Data", key="Interactive_Data_btn"):
        st.session_state.page = "Interactive Data"
    if col3.button("💬 Chatbot", key="chatbot_btn"):  # Add the new button
        st.session_state.page = "Chatbot"
   
# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Interactive Data"

# Show navigation buttons at the top
show_navigation_buttons()

# Page Navigation Logic
if st.session_state.page == "About":
    about()
elif st.session_state.page == "Interactive Data":
    show_Interactive_Data()
elif st.session_state.page == "Chatbot":  # Add the new page logic
    show_chatbot()
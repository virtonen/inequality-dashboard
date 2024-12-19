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

def show_navigation_buttons():
    col1, col2, col3 = st.columns(3)
    
    # Define button styles
    default_style = """
        <style>
        div.stButton > button {
            background-color: #ffffff;
            color: #000000;
            width: 100%;
        }
        </style>
    """
    
    active_style = """
        <style>
        div.stButton > button {
            background-color: #0066cc;
            color: #ffffff;
            width: 100%;
        }
        </style>
    """
    
    # About button
    if st.session_state.page == "About":
        col1.markdown(active_style, unsafe_allow_html=True)
    else:
        col1.markdown(default_style, unsafe_allow_html=True)
    if col1.button("🔍 About", key="about_btn"):
        st.session_state.page = "About"
    
    # Interactive Data button
    if st.session_state.page == "Interactive Data":
        col2.markdown(active_style, unsafe_allow_html=True)
    else:
        col2.markdown(default_style, unsafe_allow_html=True)
    if col2.button("📊 Interactive Data", key="Interactive_Data_btn"):
        st.session_state.page = "Interactive Data"
    
    # Chatbot button
    if st.session_state.page == "Chatbot":
        col3.markdown(active_style, unsafe_allow_html=True)
    else:
        col3.markdown(default_style, unsafe_allow_html=True)
    if col3.button("💬 Chatbot", key="chatbot_btn"):
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
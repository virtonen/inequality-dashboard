import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path
from navigation.about import about
from navigation.interactive_data import show_Interactive_Data

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
    col1, col2 = st.columns(2)  
    if col1.button("🔍 About", key="about_btn"):
        st.session_state.page = "About"
    if col2.button("📊 Interactive Data", key="Interactive_Data_btn"):  # Moved this up
        st.session_state.page = "Interactive Data"
   
# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "About"  # Changed from "Home" to "About"

# Show navigation buttons at the top
show_navigation_buttons()

# Page Navigation Logic
if st.session_state.page == "About":
    # Call About Page Content
    about()
elif st.session_state.page == "Interactive Data":
    show_Interactive_Data()
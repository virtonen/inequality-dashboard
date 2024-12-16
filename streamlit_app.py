import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path

from navigation.about_project import show_about_project
from navigation.about_us import show_about_us
from navigation.who_is_this_for import show_who_is_this_for
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
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("🏠 Home", key="home_btn"):
        st.session_state.page = "Home"
    if col2.button("🔍 About Project", key="about_project_btn"):
        st.session_state.page = "About Project"
    if col3.button("📖 About Us", key="about_us_btn"):
        st.session_state.page = "About Us"
    if col4.button("👥 Who is This For?", key="who_is_this_for_btn"):
        st.session_state.page = "Who is This For?"
    if col5.button("📊 Interactive Data", key="Interactive_Data_btn"):
        st.session_state.page = "Interactive Data"
   

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Show navigation buttons at the top
show_navigation_buttons()

# Page Navigation Logic
if st.session_state.page == "Home":
    # Render Home Page Content
    st.markdown("""
    ### Welcome!  
    Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, and **Poverty Ratios**.
    """)

elif st.session_state.page == "About Project":
    # Call About Project Page Content
    show_about_project()

elif st.session_state.page == "About Us":
    # Call About Us Page Content
    show_about_us()

elif st.session_state.page == "Who is This For?":
    # Call Who is This For Page Content
    show_who_is_this_for()

elif st.session_state.page == "Interactive Data":
    show_Interactive_Data()
    

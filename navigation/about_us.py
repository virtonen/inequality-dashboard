import streamlit as st

def show_about_project():
    # Welcome section first with h3 size
    st.markdown("""
    ### Welcome!  
    Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, and **Poverty Ratios**.
    """)
    
    # About Project section with h3 size (same as Welcome)
    st.markdown("""
    ### 🔍 About the Project
    
    This project uses data from the **World Bank** and **World Inequality Lab** to provide interactive visualizations of global economic trends.
    """)

def show_about_us():
    st.markdown("### 📖 About Us")  # Changed from title() to markdown() for consistent sizing
    st.write("""
    We created this dashboard to make economic inequality data accessible,  
    engaging, and easy to explore for everyone.
    """)

import streamlit as st

def show_about_project():
    # Welcome section
    st.markdown("### Welcome!")
    st.markdown("Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, and **Poverty Ratios**.")
    
    # Add some space between sections
    st.write("")
    
    # About Project section
    st.markdown("### 🔍 About the Project")
    st.markdown("This project uses data from the **World Bank** and **World Inequality Lab** to provide interactive visualizations of global economic trends.")


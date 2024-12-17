import streamlit as st

def about():    
    # Welcome section
    st.markdown("### Welcome!")
    st.markdown("Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, and **Poverty Ratios**.")
    
    # Add some space between sections
    st.write("")
    
    # About Project section
    st.markdown("### 🔍 About the Project")
    st.markdown("This project uses data from the **World Bank** and **World Inequality Lab** to provide interactive visualizations of global economic trends.")
    # About Us section
    st.markdown("### 📖 About Us")  
    st.write("""
    We created this dashboard to make economic inequality data accessible,  
    engaging, and easy to explore for everyone.
    """)
    
    # Add some space between sections
    st.write("")

    st.markdown("### 👥 Who is This For?")
    st.write("""
    This dashboard is for:
    - 🏛 **Policymakers**
    - 📊 **Researchers**
    - 🎓 **Students**
    """)

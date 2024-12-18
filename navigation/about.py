import streamlit as st

def about():    
    # Welcome section
    st.markdown("### Welcome!")
    st.markdown("Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, and **Poverty Ratios**.")
    
    # Add some space between sections
    st.write("")
    
    # About Project section
    st.markdown("### 🔍 About the Project")
    st.markdown("""
    This project uses data from the **World Bank** and **World Inequality Lab** to provide interactive visualizations of global economic trends.
    The dashboard includes:
    - **GDP Trends**: Visualize GDP deflator data over time for selected countries.
    - **Gini Coefficient**: Explore income inequality across different nations.
    - **Poverty Ratios**: Analyze poverty headcount ratios at $2.15 a day (2017 PPP) for various countries.
    """)
    st.markdown("### 📖 About Us")  
    st.write("""
    We created this dashboard to make economic inequality data accessible,  
    engaging, and easy to explore for everyone. We are undergraduate economics students at **Minerva University**, and this is our final project in a course about global inequality.
    """)
    
    st.markdown("### 👥 Authors")
    st.write("""
    - [Maggie Possidente](https://www.linkedin.com/in/maggie-possidente/)
    - [Yelyzaveta Radionova](https://www.linkedin.com/in/yelyzaveta-radionova/)
    - [Vladislav Virtonen](https://www.linkedin.com/in/virtonen/)
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

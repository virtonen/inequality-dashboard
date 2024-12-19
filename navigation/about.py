import streamlit as st

def about():    
    # Welcome section
    st.markdown("### Welcome!")
    st.markdown("Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, **Poverty Ratios**, and **Income Distributions**. Use the three buttons above to navigate between pages.")
    
    # Add some space between sections
    st.write("")
    
    # About Project section
    st.markdown("### 🔍 About the Project")
    st.markdown("""
    This project uses data from the **World Bank** and **The World Income Inequality Database (WIID)** to provide interactive visualizations of global economic trends.
    The 'Interactive Data' dashboard includes:
    - **GDP Trends**: Visualize GDP deflator data over time for selected countries.
    - **Gini Coefficient**: Explore income inequality across different nations.
    - **Poverty Ratios**: Analyze poverty headcount ratios at $2.15 a day (2017 PPP) for various countries.
    - **Income Quintiles**: Plot income quintiles per country to show income inequality.
    - **Income Inequality Ratios**: Compare income inequality ratios across time.
    - **Inequality Chatbot**: Chat about inequality to learn more.
    """)
    st.markdown("### 📖 About Us")  
    st.write("""
    We created this dashboard to make economic inequality data accessible, engaging, and easy to explore for everyone. We are undergraduate economics students at [**Minerva University**](http://minerva.edu), and this is our final project in a course about global inequality.
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

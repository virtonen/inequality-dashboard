import streamlit as st

def about():    
    # Welcome section
    st.markdown("### Welcome!")
    st.markdown("""
    We are so glad to have you here! This dashboard is designed to help you understanding global economic trends in an interactive and engaging way. 
    Dive into topics like **GDP Trends**, **Income Inequality**, **Poverty Ratios**, and **Income Distributions**. Use the buttons above to explore 
    our visualizations!
    """)

    
    # Add some space between sections
    st.write("")
    
    # About Project section
    st.markdown("### 🔍 About the Project")
    st.markdown("""
    This dashboard is built with the aim of transforming complex economic data into accessible, interactive visualizations that anyone can understand and explore. Economic inequality is a pressing global issue, but understanding it often requires navigating dense data sets and technical jargon. This project seeks to bridge that gap by presenting critical data in a way that is clear, engaging, and actionable.

    We use the data sources of the **World Bank** and the **World Income Inequality Database (WIID)** to provide insights into various economic indicators. Through our visualizations, you can explore topics such as:

    - **GDP Trends**: Understand how the GDP deflator has changed over time and across countries, offering a glimpse into inflationary trends and economic growth.
    - **Gini Coefficient**: Dive into one of the most commonly used measures of income inequality, comparing how wealth is distributed across different nations.
    - **Poverty Ratios**: Examine poverty levels globally, specifically focusing on the percentage of populations living under $2.15 a day (2017 PPP). 
    - **Income Quintiles**: Visualize the distribution of income within countries to understand inequality at a granular level.
    - **Income Inequality Ratios**: Analyze changes in income disparity over time to identify trends and patterns.
    - **Inequality Chatbot**: Engage with an AI chatbot to learn more about economic inequality, its causes, and potential solutions in an interactive way.

    At its core, this project aims to make global inequality data more approachable and useful to people from diverse backgrounds. Whether you're a policymaker looking to shape impactful strategies, a student wanting to deepen your understanding of inequality, or simply a curious individual, this dashboard is here to support your journey of discovery.
    """)
    
    st.markdown("### 📖 About Us")  
    st.write("""
    We created this dashboard to make economic inequality data accessible, engaging, and easy to explore for everyone. We are undergraduate students studying economics at [**Minerva University**](http://minerva.edu), and this dashboard is our final project in a course about global inequality.
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
    This dashboard is designed to serve a wide range of users, each with unique needs and goals. Here’s how different groups can benefit from it:

    - **📊 Researchers**: Whether you're an academic or a professional researcher, this tool can help you explore economic trends, test hypotheses, and uncover patterns that may not be immediately obvious. The interactive nature of the dashboard allows you to customize your analysis and dig deep into the data.

    - **🎓 Students**: For students of economics, sociology, or related fields, the dashboard offers a hands-on way to engage with complex data. It’s a great resource for understanding key concepts like GDP, income inequality, and poverty, and for applying these ideas to real-world examples.
    
    - **🏛 Policymakers**: As a policymaker, you can use the dashboard to gain a clearer understanding of economic inequality and its implications. The visualizations can inform decisions on creating fairer tax policies, improving social welfare programs, and addressing systemic inequalities.

    - **🌍 Activists and Advocates**: If you're working to address inequality on the ground, this tool can help you build a stronger case for change. Use the data to highlight disparities and advocate for policies that promote equity.

    - **🧠 Educators**: Teachers and professors can use this dashboard as a teaching tool to help students understand global inequality. The visualizations can serve as discussion prompts or as a basis for assignments and projects.

    - **💡 Curious Individuals**: Even if you’re not a professional in the field, this dashboard is for anyone who wants to learn more about the world we live in. It’s an accessible way to explore topics like income distribution, poverty, and inequality, and to understand their significance in a global context.
    

    This dashboard is for anyone who believes that understanding inequality is the first step towards creating a more equitable world. Whether you’re here for academic, professional, or personal reasons, we hope it provides the clarity and insight you’re looking for!
    """)

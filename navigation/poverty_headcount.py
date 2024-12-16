import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path


# POVERTY DATA

def get_poverty_data():
    """Grab Poverty Headcount Ratio data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent/'data/poverty_headcount_ratio_data.csv'
    raw_poverty_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2023

    # Melt the dataset into long format
    poverty_df = raw_poverty_df.melt(
        id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
        var_name='Year',
        value_name='Poverty Headcount Ratio'
    )

    # Convert Year to numeric and drop rows with missing Poverty Headcount Ratio values
    poverty_df['Year'] = pd.to_numeric(poverty_df['Year'], errors='coerce')
    poverty_df = poverty_df.dropna(subset=['Poverty Headcount Ratio'])

    return poverty_df

poverty_df = get_poverty_data()

def null_perc(df) : 
    percent_missing = df.isnull().sum() * 100 / len(df) 
    missing_value_df = pd.DataFrame({
                                    'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True , ascending=False)
    #print(missing_value_df)
    return missing_value_df 






# Interactive visualization for the Poverty Headcount Ratio

st.header('Poverty Headcount Ratio over time', divider='gray')

# Poverty Headcount Ratio Dataset Information
st.markdown("""
#### About Poverty Headcount Ratio Data
- **Source**: World Bank, Poverty and Inequality Platform.
- **Indicator**: Poverty headcount ratio at $2.15 a day (2017 PPP).
- **Description**: Data are based on primary household survey data obtained from government statistical agencies and World Bank country departments. High-income economies' data are primarily from the Luxembourg Income Study database. More info at [pip.worldbank.org](https://pip.worldbank.org).

#### Absolute Poverty
The absolute poverty headcount ratio measures the percentage of a country's population living below the international poverty line, currently set at $1.90 per day. This metric provides insight into the level of extreme income poverty within a country.

#### Absolute vs Relative Poverty
Absolute poverty refers to a lack of access to the basic necessities for human survival, such as adequate food, clean water, sanitation, health care, and shelter. The absolute poverty headcount ratio measures the percentage of a population living below an established poverty line, currently set at $1.90 per day by the World Bank. This provides insight into the level of extreme income deprivation within a country.

Relative poverty, on the other hand, is a measure of income inequality. The Gini coefficient is a commonly used metric for relative poverty, as it shows how income or wealth is distributed across a population. A high Gini indicates greater inequality, even if most people are above the absolute poverty line. Relative poverty compares an individual's or household's income to the overall distribution, rather than against a fixed poverty threshold.

In contrast, the Gini coefficient is a measure of relative income inequality, showing how income/wealth is distributed across a population. A high Gini indicates greater inequality but does not necessarily mean high levels of absolute poverty. Analyzing both absolute poverty and relative inequality can provide a more complete picture of a country's socioeconomic conditions.
""")

# Filter years and countries for poverty data
poverty_min_year = poverty_df['Year'].min()
poverty_max_year = poverty_df['Year'].max()

poverty_from_year, poverty_to_year = st.slider(
    'Which years are you interested in for poverty data?',
    min_value=int(poverty_min_year),
    max_value=int(poverty_max_year),
    value=[int(poverty_min_year), int(poverty_max_year)]
)

poverty_countries = poverty_df['Country Name'].unique()
selected_poverty_countries = st.multiselect(
    'Which countries would you like to view for poverty data?',
    poverty_countries,
    ['Argentina', 'Chile', 'Ethiopia']  # Add any defaults you prefer
)
# Filter the Poverty Data
filtered_poverty_df = poverty_df[
    (poverty_df['Country Name'].isin(selected_poverty_countries))
    & (poverty_df['Year'] <= poverty_to_year)
    & (poverty_df['Year'] >= poverty_from_year)
]


poverty_chart = alt.Chart(filtered_poverty_df).mark_line().encode(
    x=alt.X('Year:O', title='Year'),  # No commas in Year
    y=alt.Y('Poverty Headcount Ratio', title='Headcount Ratio (%)'),
    color='Country Name:N',  # Use Country Name for legend
    tooltip=['Country Name', 'Year', 'Poverty Headcount Ratio']
).properties(
    title='Poverty Headcount Ratio at $2.15/day (2017 PPP)'
)

st.altair_chart(poverty_chart, use_container_width=True)

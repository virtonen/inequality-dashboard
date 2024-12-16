import streamlit as st
import pandas as pd
import altair as alt
import math
from pathlib import Path
import os

# Function to load Gini data
@st.cache_data
def get_gini_data():
    """Load and process Gini data from a CSV file."""
    DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
    DATA_FILENAME = os.path.join(DATA_DIR, 'gini_data.csv')
    try:
        raw_gini_df = pd.read_csv(DATA_FILENAME)
    except FileNotFoundError:
        st.error(f"Data file not found: {DATA_FILENAME}. Please ensure the file exists.")
        return pd.DataFrame()

    gini_df = raw_gini_df.melt(
        ['Country Name', 'Country Code'],
        var_name='Year',
        value_name='GINI'
    )
    gini_df['Year'] = pd.to_numeric(gini_df['Year'], errors='coerce')
    return gini_df

# Load the Gini data
gini_df = get_gini_data()

# Function to calculate null percentages
def null_perc(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    return missing_value_df

# Main function to show Gini Coefficient page
def show_gini_coefficient():
    st.markdown(r"""
    ## Gini Coefficient

    The **Gini coefficient** is a measure of statistical dispersion intended to represent
    the income inequality or wealth inequality within a nation or a social group.
    It is the most commonly used measure of inequality. A Gini coefficient of 0
    represents perfect equality, while a Gini coefficient of 100 implies perfect inequality.
    """)

    # Add some spacing
    ''
    ''

    # Show the DataFrame
    st.subheader("Data: ")
    if gini_df.empty:
        st.error("No data to display. Please check the file path or data file.")
    else:
        st.write(gini_df)

    # Show null values
    st.subheader("Null values: ")
    st.write(null_perc(gini_df))

    # Slider for year range
    min_value = int(gini_df['Year'].min())
    max_value = int(gini_df['Year'].max())
    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value]
    )

    # Multiselect for countries
    countries = gini_df['Country Name'].unique()
    selected_countries = st.multiselect(
        'Which countries would you like to view?',
        countries,
        ['Germany', 'Brazil', 'Norway', 'South Africa', 'United States', 'Estonia']
    )

    # Filter the data
    filtered_gini_df = gini_df[
        (gini_df['Country Name'].isin(selected_countries)) &
        (gini_df['Year'] >= from_year) &
        (gini_df['Year'] <= to_year)
    ]

    st.header('Gini over time', divider='gray')

    # Plot the chart
    if filtered_gini_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        gini_chart = alt.Chart(filtered_gini_df).mark_line().encode(
            x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),
            y=alt.Y('GINI', title='GINI'),
            color='Country Name:N',
            tooltip=['Country Name', 'Year', 'GINI']
        ).properties(
            title='Gini Coefficient over Time'
        )
        st.altair_chart(gini_chart, use_container_width=True)

    # Metrics for selected countries
    st.header(f'Gini in {to_year}', divider='gray')

    st.markdown("""
    **Explanation:**  
    The metrics below display the Gini coefficients for the selected countries in the chosen year. Each metric shows the current Gini value and the change from the first year in the selected range, indicating whether inequality has increased or decreased.
    """)

    cols = st.columns(4)
    first_year = gini_df[gini_df['Year'] == from_year]
    last_year = gini_df[gini_df['Year'] == to_year]

    for i, country in enumerate(selected_countries):
        col = cols[i % len(cols)]
        with col:
            first_gini = first_year[first_year['Country Name'] == country]['GINI'].iat[0] if not first_year[first_year['Country Name'] == country].empty else None
            last_gini = last_year[last_year['Country Name'] == country]['GINI'].iat[0] if not last_year[last_year['Country Name'] == country].empty else None

            # Handle missing values
            if first_gini is None or math.isnan(first_gini) or last_gini is None or math.isnan(last_gini):
                growth = 'n/a'
                delta_color = 'off'
                display_gini = 'n/a'
            else:
                growth = f'{last_gini - first_gini:.2f}'
                delta_color = 'inverse' if last_gini < first_gini else 'normal'
                display_gini = f'{last_gini:.2f}'

            st.metric(
                label=f'{country} GINI',
                value=display_gini,
                delta=growth,
                delta_color=delta_color
            )

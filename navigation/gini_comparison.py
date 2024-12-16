import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

def show_gini_comparison():
    st.title("📊 Gini Comparison")
    st.write("This page allows you to compare Gini Coefficients between countries.")
    # Add any specific code or visualization related to Gini Comparison
# GINI DATA
# Declare some useful functions.

@st.cache_data
def get_gini_data():
    """Grab GINI data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gini_data.csv'
    raw_gini_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2023

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GINI for 1960
    # - GINI for 1961
    # - GINI for 1962
    # - ...
    # - GINI for 2023
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GINI
    #
    # So let's pivot all those year-columns into two: Year and GINI
    gini_df = raw_gini_df.melt(
        ['Country Name','Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GINI',
    )

    # Convert years from string to integers
    gini_df['Year'] = pd.to_numeric(gini_df['Year'])

    return gini_df

gini_df = get_gini_data()

# -----------------------------------------------------------------------------
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




# -----------------------------------------------------------------------------
# Draw the actual page

st.header('GDP Comparison', divider='gray')
st.markdown("""
Some insigths about GDP data""")

# GDP DATA
def get_gdp_deflator_data():
    """Grab GDP deflator data from the world_bank_popular_indicators dataset."""
    DATA_FILENAME = Path(__file__).parent/'data/world_bank_popular_indicators.csv'
    raw_gdp_deflator_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 2000
    MAX_YEAR = 2015

    # Filter the dataset for the specific Series Code
    gdp_deflator_df = raw_gdp_deflator_df[raw_gdp_deflator_df['Series Code'] == 'NY.GDP.DEFL.KD.ZG']

    # Melt the dataset into long format
    gdp_deflator_df = gdp_deflator_df.melt(
        id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
        var_name='Year',
        value_name='GDP Deflator'
    )

    # Convert Year to numeric and drop rows with missing GDP Deflator values
    gdp_deflator_df['Year'] = gdp_deflator_df['Year'].str.extract('(\d{4})').astype(int)
    gdp_deflator_df = gdp_deflator_df.dropna(subset=['GDP Deflator'])

    return gdp_deflator_df

gdp_deflator_df = get_gdp_deflator_data()

# Show first 5 rows (default)
gdp_deflator_df.head()

# Show specific number of rows (e.g., first 10 rows)
print(gdp_deflator_df.head(300))

# Filter years and countries for GDP deflator data
gdp_min_year = gdp_deflator_df['Year'].min()
gdp_max_year = gdp_deflator_df['Year'].max()

gdp_from_year, gdp_to_year = st.slider(
    'Which years are you interested in for GDP deflator data?',
    min_value=gdp_min_year,
    max_value=gdp_max_year,
    value=[gdp_min_year, gdp_max_year]
)

gdp_countries = gdp_deflator_df['Country Name'].unique()
selected_gdp_countries = st.multiselect(
    'Which countries would you like to view for GDP deflator data?',
    gdp_countries,
    ['United States', 'China', 'India']  # Add any defaults you prefer
)

# Filter the GDP Deflator Data
filtered_gdp_deflator_df = gdp_deflator_df[
    (gdp_deflator_df['Country Name'].isin(selected_gdp_countries))
    & (gdp_deflator_df['Year'] <= gdp_to_year)
    & (gdp_deflator_df['Year'] >= gdp_from_year)
]

gdp_deflator_chart = alt.Chart(filtered_gdp_deflator_df).mark_line().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),  # No decimals in Year
    y=alt.Y('GDP Deflator', 
            title='GDP Deflator (%)',
            axis=alt.Axis(format='.2f')),  # Format specified in axis
    color='Country Name:N',
    tooltip=['Country Name', 'Year', 'GDP Deflator']
).properties(
    title='GDP Deflator over time'
)
st.altair_chart(gdp_deflator_chart, use_container_width=True)
# Variable selector for indicators
indicator_df = pd.read_csv(Path(__file__).parent/'data/world_bank_popular_indicators.csv')

# Melt the dataset into long format
indicator_long_df = indicator_df.melt(
    id_vars=['Series Name', 'Series Code', 'Country Name', 'Country Code'],
    value_vars=[col for col in indicator_df.columns if 'YR' in col],
    var_name='Year',
    value_name='Value'
)

# Convert Year to numeric
indicator_long_df['Year'] = indicator_long_df['Year'].str.extract('(\d{4})').astype(int)

st.header('Visualize Your Own Variable', divider='gray')

# Select Series Name
series_names = indicator_long_df['Series Name'].unique()
selected_series = st.selectbox('Select a Variable', series_names)

# Filter data based on selected series
filtered_indicator_df = indicator_long_df[indicator_long_df['Series Name'] == selected_series]

# Slider for years
indicator_min_year = filtered_indicator_df['Year'].min()
indicator_max_year = filtered_indicator_df['Year'].max()

indicator_from_year, indicator_to_year = st.slider(
    'Which years are you interested in?',
    min_value=int(indicator_min_year),
    max_value=int(indicator_max_year),
    value=[int(indicator_min_year), int(indicator_max_year)]
)

# Multiselect for countries
indicator_countries = filtered_indicator_df['Country Name'].unique()
selected_indicator_countries = st.multiselect(
    'Which countries would you like to view?',
    indicator_countries,
    ['United States', 'China', 'India']  # Add any defaults you prefer
)

# Filter the data
filtered_indicator_df = filtered_indicator_df[
    (filtered_indicator_df['Country Name'].isin(selected_indicator_countries)) &
    (filtered_indicator_df['Year'] <= indicator_to_year) &
    (filtered_indicator_df['Year'] >= indicator_from_year)
]

# Create the chart
indicator_chart = alt.Chart(filtered_indicator_df).mark_line().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d', grid=True)),
    y=alt.Y('Value', title=selected_series, axis=alt.Axis(format=',.0f', tickCount=5, grid=True)),
    color='Country Name:N',
    tooltip=['Country Name', 'Year', 'Value']
).properties(
    title=f'{selected_series} over Time'
).configure_axis(
    gridDash=[5,5],
    gridOpacity=0.5
)

st.altair_chart(indicator_chart, use_container_width=True)

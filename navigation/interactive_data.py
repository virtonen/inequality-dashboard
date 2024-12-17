import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path

# Cache decorators for each data loading function
@st.cache_data
def get_gdp_data():
    """Grab GDP deflator data from the world_bank_popular_indicators dataset."""
    DATA_FILENAME = Path(__file__).parent.parent/'data/world_bank_popular_indicators.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 2000
    MAX_YEAR = 2015

    # Filter the dataset for the specific Series Code
    gdp_deflator_df = raw_gdp_df[raw_gdp_df['Series Code'] == 'NY.GDP.DEFL.KD.ZG']

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

@st.cache_data
def get_gini_data():
    """Grab GINI data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent.parent/'data/gini_data.csv'
    raw_gini_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2023

    gini_df = raw_gini_df.melt(
        ['Country Name','Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GINI',
    )

    # Convert years from string to integers
    gini_df['Year'] = pd.to_numeric(gini_df['Year'])

    return gini_df

@st.cache_data
def get_poverty_data():
    """Grab Poverty Headcount Ratio data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent.parent/'data/poverty_headcount_ratio_data.csv'
    raw_poverty_df = pd.read_csv(DATA_FILENAME)

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

def null_perc(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    return missing_value_df


def show_Interactive_Data():
    st.header('GDP Comparison', divider='gray')
    st.markdown("""Some insights about GDP data""")
    
    gdp_deflator_df = get_gdp_data()

    # Filter years and countries for GDP deflator data
    gdp_min_year = gdp_deflator_df['Year'].min()
    gdp_max_year = gdp_deflator_df['Year'].max()

    gdp_from_year, gdp_to_year = st.slider(
        'Which years are you interested in for GDP deflator data?',
        min_value=int(gdp_min_year),  # Convert to integer
        max_value=int(gdp_max_year),  # Convert to integer
        value=[int(gdp_min_year), int(gdp_max_year)],  # Convert default range to integers
        step=1  # Ensure step is an integer
    )

    gdp_countries = gdp_deflator_df['Country Name'].unique()
    selected_gdp_countries = st.multiselect(
        'Which countries would you like to view for GDP deflator data?',
        gdp_countries,
        ['United States', 'China', 'India']
    )

    # Filter the GDP Deflator Data
    filtered_gdp_deflator_df = gdp_deflator_df[
        (gdp_deflator_df['Country Name'].isin(selected_gdp_countries))
        & (gdp_deflator_df['Year'] <= gdp_to_year)
        & (gdp_deflator_df['Year'] >= gdp_from_year)
    ]

    gdp_deflator_chart = alt.Chart(filtered_gdp_deflator_df).mark_line().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),
        y=alt.Y('GDP Deflator:Q', 
                title='GDP Deflator (%)',
                axis=alt.Axis(format='d', tickCount=5)),  # Show integers instead of floats
        color='Country Name:N',
        tooltip=['Country Name', 'Year', 'GDP Deflator']
    ).properties(
        title='GDP Deflator over time'
    )
    st.altair_chart(gdp_deflator_chart, use_container_width=True)

    # Variable selector for indicators
    indicator_df = pd.read_csv(Path(__file__).parent.parent/'data/world_bank_popular_indicators.csv')

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
        ['United States', 'China', 'India']
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
        y=alt.Y('Value:Q', title=selected_series, axis=alt.Axis(format=',.0f', tickCount=5, grid=True)),
        color='Country Name:N',
        tooltip=['Country Name', 'Year', 'Value']
    ).properties(
        title=f'{selected_series} over Time'
    ).configure_axis(
        gridDash=[5,5],
        gridOpacity=0.5
    )

    st.altair_chart(indicator_chart, use_container_width=True)



    # Gini Coefficient Section
    gini_df = get_gini_data()
    st.header(f'Gini Coefficient', divider='gray')
    st.markdown(r"""

The **Gini coefficient** is a measure of statistical dispersion intended to represent
the income inequality or wealth inequality within a nation or a social group.
It is the most commonly used measure of inequality. A Gini coefficient of 0
represents perfect equality, where everyone has the same income, while a Gini
coefficient of 100 implies perfect inequality, where one person has all the income
and everyone else has none. Most countries have Gini coefficients between 25-60, 
with lower values indicating more equality and higher values indicating more inequality.

## Relation to the Lorenz Curve
The Gini coefficient is derived from the [Lorenz curve](https://en.wikipedia.org/wiki/Lorenz_curve),
which graphically represents the distribution of income or wealth within a population.
The Gini coefficient is defined as the ratio of the area between the Lorenz curve and the line of equality
to the total area under the line of equality.

## Calculation Formula

The Gini coefficient ($G$) can be calculated using the following formula:

$$
G = \frac{A}{A + B}
$$

where:
- A is the area between the line of equality and the Lorenz curve.
- B is the area under the Lorenz curve.

Alternatively, it can be calculated using the formula:

$$
G = \frac{1}{n^2 \mu} \sum_{i=1}^{n} \sum_{j=1}^{n} |x_i - x_j|
$$

where:
- n is the number of observations.
- $\mu$ is the mean of the distribution.
- $x_i$ and $x_j$ are individual values.

This dashboard reads Gini coefficient data from a CSV file obtained from the [World Bank Open Data](https://data.worldbank.org/),
which contains Gini coefficients for various countries over a range of years.
""")

    st.subheader("Data: ")
    st.write(gini_df)
    
    st.subheader("Null values: ")
    st.write(null_perc(gini_df))

    min_value = gini_df['Year'].min()
    max_value = gini_df['Year'].max()

    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value])

    countries = gini_df['Country Name'].unique()

    if not len(countries):
        st.warning("Select at least one country")

    selected_countries = st.multiselect(
        'Which countries would you like to view?',
        countries,
        ['Germany', 'Brazil', 'Norway', 'South Africa', 'United States', 'Estonia'])

    # Filter the data
    filtered_gini_df = gini_df[
        (gini_df['Country Name'].isin(selected_countries))
        & (gini_df['Year'] <= to_year)
        & (from_year <= gini_df['Year'])
    ]

    st.header('Gini over time', divider='gray')

    gini_chart = alt.Chart(filtered_gini_df).mark_line().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),
        y=alt.Y('GINI:Q', title='GINI', axis=alt.Axis(format=',.0f', tickCount=5)),
        color='Country Name:N',
        tooltip=['Country Name', 'Year', 'GINI']
    ).properties(
        title='Gini Coefficient over Time'
    )

    st.altair_chart(gini_chart, use_container_width=True)

    first_year = gini_df[gini_df['Year'] == from_year]
    last_year = gini_df[gini_df['Year'] == to_year]

    st.header(f'Gini in {to_year}', divider='gray')

    st.markdown("""
    **Explanation:**  
    The metrics below display the Gini coefficients for the selected countries in the chosen year. Each metric shows the current Gini value and the change from the first year in the selected range, indicating whether inequality has increased or decreased.
    """)

    cols = st.columns(4)

    for i, country in enumerate(selected_countries):
        col = cols[i % len(cols)]

        with col:
            # Get Gini values for the selected country
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

    # Poverty Section
    st.header('Poverty Headcount Ratio over time', divider='gray')

    poverty_df = get_poverty_data()

    # Poverty Headcount Ratio Dataset Information
    st.markdown("""
    #### About Poverty Headcount Ratio Data
    - **Source**: World Bank, Poverty and Inequality Platform.
    - **Indicator**: Poverty headcount ratio at $2.15 a day (2017 PPP).
    - **Description**: Data are based on primary household survey data obtained from government statistical agencies and World Bank country departments. High-income economies' data are primarily from the Luxembourg Income Study database. More info at [pip.worldbank.org](https://pip.worldbank.org).
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
        ['Argentina', 'Chile', 'Ethiopia']
    )
    
    # Filter the Poverty Data
    filtered_poverty_df = poverty_df[
        (poverty_df['Country Name'].isin(selected_poverty_countries))
        & (poverty_df['Year'] <= poverty_to_year)
        & (poverty_df['Year'] >= poverty_from_year)
    ]

    poverty_chart = alt.Chart(filtered_poverty_df).mark_line().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Poverty Headcount Ratio:Q', title='Headcount Ratio (%)', axis=alt.Axis(format=',.0f', tickCount=5)),
        color='Country Name:N',
        tooltip=['Country Name', 'Year', 'Poverty Headcount Ratio']
    ).properties(
        title='Poverty Headcount Ratio at $2.15/day (2017 PPP)'
    )

    st.altair_chart(poverty_chart, use_container_width=True)

def new_func(filtered_gdp_deflator_df):
    gdp_deflator_chart = alt.Chart(filtered_gdp_deflator_df).mark_line().encode(
        x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),
        y=alt.Y('GDP Deflator', 
                title='GDP Deflator (%)',
                axis=alt.Axis(format='.2f')),
        color='Country Name:N',
        tooltip=['Country Name', 'Year', 'GDP Deflator']
    ).properties(
        title='GDP Deflator over time'
    )
    st.altair_chart(gdp_deflator_chart, use_container_width=True)

if __name__ == "__main__":
    show_Interactive_Data()

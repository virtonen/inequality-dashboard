import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path
import plotly.graph_objects as go

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

@st.cache_data
def get_wiid_data():
    """Grab WIID (World Income Inequality Database) data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent.parent/'data/WIID_data.csv'
    wiid_df = pd.read_csv(DATA_FILENAME)
    
    # Convert numeric columns
    numeric_columns = ['gini', 'mean', 'median', 'gdp', 'population']
    for col in numeric_columns:
        wiid_df[col] = pd.to_numeric(wiid_df[col], errors='coerce')
    
    # Convert year to integer
    wiid_df['year'] = pd.to_numeric(wiid_df['year'], errors='coerce')
    
    # Drop rows with missing key values
    wiid_df = wiid_df.dropna(subset=['country', 'year', 'gini'])
    
    return wiid_df

# -----------------#
# PAGE STARTS HERE

def show_Interactive_Data():
    st.header('GDP Deflator Comparison', divider='gray')
    st.markdown("""
    ### Understanding the GDP Deflator

    You probably have heard about inflation, but have you heard about the GDP Deflator? Every economy's price levels are changing differently, and the GDP Deflator is one way to represent how differently (or unequally) our economies are developing.

    #### What is the GDP Deflator?
    The **GDP Deflator** is a measure of the level of prices of all new, domestically produced, final goods and services in an economy. It is calculated as follows:

    $$
    \\text{GDP Deflator} = \\frac{\\text{Nominal GDP}}{\\text{Real GDP}} \\times 100
    $$

    #### Why is it Important?
    - **Comprehensive Measure**: Unlike the Consumer Price Index (CPI), the GDP Deflator includes all goods and services produced domestically, providing a broader measure of inflation.
    - **Economic Analysis**: It helps economists and policymakers understand the inflationary pressures within the economy and make informed decisions regarding monetary policy.

    #### Strengths
    - **Broad Coverage**: Includes all domestically produced goods and services.
    - **Reflects Changes in Consumption and Investment**: Adjusts for changes in consumption patterns and investment, providing a more accurate measure of inflation over time.

    #### Limitations
    - **Data Lag**: The GDP Deflator is typically released quarterly, which may not provide the most up-to-date picture of inflation.
    - **Complex Calculation**: Requires comprehensive data on all goods and services produced, which can be complex and resource-intensive to gather.

    This dashboard allows you to explore the GDP Deflator data across different countries and years, providing insights into how inflation has evolved over time. Use the interactive tools to filter the data by year and country, and visualize the trends through dynamic charts and maps.

    More inequality measures follow in the next sections.
    """)

    # Preview the GDP Deflator dataset
    st.subheader("Data: ")
    st.markdown("""
    #### Data Source
    The data presented here is sourced from the [World Bank](https://databank.worldbank.org/indicator/SP.POP.TOTL/1ff4a498/Popular-Indicators). The World Development Indicators (WDI) is the primary World Bank collection of development indicators, compiled from officially recognized international sources. It presents the most current and accurate global development data available, and includes national, regional, and global estimates.
    """)
    gdp_deflator_df = get_gdp_data()
    st.write(gdp_deflator_df)
    
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

    # MAP
    # Get the unique years and countries in the data
    years = gdp_deflator_df['Year'].unique()
    countries = sorted(gdp_deflator_df['Country Name'].unique())  # Sort countries alphabetically for clarity

    # Allow the user to select a single year
    selected_year = st.select_slider(
        'Select the year',
        options=sorted(years),
        value=int(years.min())
    )

    # Checkbox to select all or none of the countries
    select_all = st.checkbox('Select all countries', value=True)

    # Multiselect widget for countries
    if select_all:
        selected_countries = countries  # If the checkbox is checked, select all countries
    else:
        selected_countries = st.multiselect(
            'Select the countries',
            options=countries,  # Dynamically populate from dataset
            default=[]  # Start with no countries selected when checkbox is unchecked
        )

    # Filter the data for the selected year and countries
    gdp_deflator_year_df = gdp_deflator_df[
        (gdp_deflator_df['Year'] == selected_year) &
        (gdp_deflator_df['Country Name'].isin(selected_countries))
    ]

    # Create the choropleth map
    world_map = new_func1(gdp_deflator_year_df)

    # Update the layout for the map
    world_map.update_layout(
        title_text=f'GDP Deflator in {selected_year}',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.5,
            y=-0.1,
            xref='paper',
            yref='paper',
            text='Source: World Inequality Database',
            showarrow=False
        )]
    )

    # Display the map in the Streamlit app
    st.plotly_chart(world_map, use_container_width=True, config={'scrollZoom': True})

    #-----------------#

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

    #### Why is the Poverty Headcount Ratio Important?
    The **Poverty Headcount Ratio** is a critical measure of inequality that captures aspects of economic disparity that the Gini coefficient and GDP Deflator do not. While the Gini coefficient provides a broad measure of income inequality and the GDP Deflator reflects inflationary pressures, the Poverty Headcount Ratio directly measures the proportion of a population living below the poverty line, offering a more tangible and human-centric view of economic hardship.

    - **Human Impact**: Unlike the Gini coefficient, which can sometimes obscure the real-life implications of inequality, the Poverty Headcount Ratio highlights the actual number of people struggling to meet basic needs.
    - **Economic Development**: The GDP Deflator measures price changes in an economy, but it does not account for how these changes affect the poorest segments of society. The Poverty Headcount Ratio provides insight into whether economic growth is inclusive and benefits the most vulnerable populations.
    - **Policy Relevance**: Policymakers can use the Poverty Headcount Ratio to design targeted interventions aimed at poverty reduction, ensuring that economic policies are inclusive and equitable.

    This metric is essential for understanding the depth and breadth of poverty within a country, making it a vital tool for assessing the effectiveness of poverty alleviation programs and economic policies.
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
    # Income Distribution by Quintiles

    # Load and prepare WIID data
    wiid_df = get_wiid_data()

    st.header('Income Distribution by Quintiles', divider='gray')
    st.markdown("""
    The **quintile shares** indicate the percentage of total income held by each 20% of the population. This visualization allows you to explore how income is distributed across different countries and time periods.
    If the quintile plot does not show your selected country, then the data for that country for the given year is not available.
    """)

    # First get available years
    available_years = sorted(wiid_df['year'].unique())
    if not available_years:
        st.warning("No data available")
        st.stop()

    # Year selector comes first
    selected_year = st.select_slider(
        'Select Year for Visualization',
        options=available_years,
        value=available_years[-1]
    )

    # Filter countries that have data for the selected year
    available_countries = sorted(wiid_df[wiid_df['year'] == selected_year]['country'].unique())
    
    # Country selector with only available countries
    selected_wiid_countries = st.multiselect(
        'Select Countries',
        options=available_countries,
        default=[
            country for country in ['Latvia', 'Estonia', 'Costa Rica', 'Bhutan', 'Belgium', 'Austria', 'Ecuador', 'Cyprus', 'Denmark']
            if country in available_countries
        ] if available_countries else []
    )

    if not selected_wiid_countries:
        st.warning("Please select at least one country to view income distribution data.")
        st.stop()

    # Filter the data by selected countries and year
    filtered_wiid_df = wiid_df[
        (wiid_df['country'].isin(selected_wiid_countries)) &
        (wiid_df['year'] == selected_year)
    ]

    # Ensure the quintile columns are numeric
    quintile_cols = ['q1', 'q2', 'q3', 'q4', 'q5']
    filtered_wiid_df[quintile_cols] = filtered_wiid_df[quintile_cols].apply(pd.to_numeric, errors='coerce')

    # Create a cleaner view of quintile data
    quintile_data = filtered_wiid_df[['country', 'year'] + quintile_cols].dropna()
    
    if quintile_data.empty:
        st.warning("No quintile data available for the selected countries and year.")
    else:
        # Melt the dataframe for visualization
        melted_wiid_df = quintile_data.melt(
            id_vars=['country', 'year'],
            value_vars=quintile_cols,
            var_name='Quintile',
            value_name='Income Share'
        )

        # Create more readable quintile labels
        melted_wiid_df['Quintile'] = pd.Categorical(
            melted_wiid_df['Quintile'].map({
                'q1': 'Bottom 20%',
                'q2': 'Lower Middle 20%',
                'q3': 'Middle 20%',
                'q4': 'Upper Middle 20%',
                'q5': 'Top 20%'
            }),
            categories=['Bottom 20%', 'Lower Middle 20%', 'Middle 20%', 'Upper Middle 20%', 'Top 20%'],
            ordered=True
        )

        # Create the Altair chart with stacked bars
        quintile_chart = alt.Chart(melted_wiid_df).mark_bar().encode(
            x=alt.X('country:N', title='Country'),
            y=alt.Y('Income Share:Q', 
               title='Income Share (%)', 
               stack='normalize',
               axis=alt.Axis(format='.1f')),
            color=alt.Color('Quintile:N', 
                  title='Income Group',
                  scale=alt.Scale(scheme='spectral'),
                  sort=['Bottom 20%', 'Lower Middle 20%', 'Middle 20%', 'Upper Middle 20%', 'Top 20%']),
            tooltip=[
            alt.Tooltip('country:N', title='Country'),
            alt.Tooltip('year:Q', title='Year'),
            alt.Tooltip('Quintile:N', title='Income Group'),
            alt.Tooltip('Income Share:Q', title='Share', format='.1f')
            ]
        ).properties(
            title=f'Income Distribution by Quintile ({selected_year})',
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16
        )

        st.altair_chart(quintile_chart, use_container_width=True)

def new_func1(gdp_deflator_year_df):
    world_map = go.Figure(data=go.Choropleth(
        locations=gdp_deflator_year_df['Country Code'],
        z=gdp_deflator_year_df['GDP Deflator'],
        text=gdp_deflator_year_df['Country Name'],
        # Use colorblind-friendly diverging colorscale centered at 0
        colorscale='RdBu',  # Red-Blue diverging colorscale that works well for colorblind viewers
        zmid=0,  # Center the color scale at 0
        autocolorscale=False,
        reversescale=True,  # Makes blue represent positive values, red negative
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title="GDP Deflator (%)"
    ))
    
    return world_map

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

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
    """Grab Gini data from a CSV file."""
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
    st.markdown("<h2 style='text-align: center;'>📊 Interactive Data Page</h2>", unsafe_allow_html=True)
    st.divider()
    st.header('Table of Contents')
    st.markdown("""
    - [GDP Deflator Comparison](#gdp-deflator-comparison)
    - [Visualize Your Own Variable](#visualize-your-own-variable)
    - [Gini Coefficient](#gini-coefficient)
    - [Poverty Headcount Ratio](#poverty-headcount-ratio)
    - [Income Distribution by Quintiles](#income-distribution-by-quintiles)
    - [Income Inequality Ratios](#income-inequality-ratios)
    """)
    st.header('GDP Deflator Comparison', divider='gray')
    st.markdown("""
    ### Understanding the GDP Deflator

    You probably have heard about inflation, but have you heard about the GDP Deflator? Every economy's price levels are changing differently, and the GDP Deflator is one way to represent how differently (or unequally) our economies are developing.

    #### What is the GDP Deflator?
    A [GDP deflator](https://study.com/academy/lesson/gdp-deflator-definition-formula-example.html#:~:text=A%20GDP%20deflator%20is%20a%20tool%20that%20is%20used%20to,services%20produced%20in%20an%20economy.) is a tool used to measure price changes over time to compare the current prices with historical prices accurately. It is calculated as follows:

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

    """)

    # Preview the GDP Deflator dataset
    st.subheader("Data")
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
    # Create a base dataframe with all country codes and zero values for GDP Deflator
    base_df = pd.DataFrame({
        'Country Code': gdp_deflator_df['Country Code'].unique(),
        'Country Name': gdp_deflator_df['Country Name'].unique(),
        'GDP Deflator': [0] * len(gdp_deflator_df['Country Code'].unique())
    })

    # If countries are selected, update the values for those countries
    if selected_countries:
        gdp_deflator_year_df = gdp_deflator_df[
            (gdp_deflator_df['Year'] == selected_year) &
            (gdp_deflator_df['Country Name'].isin(selected_countries))
        ]
        # Update base_df with actual values where available
        for idx, row in gdp_deflator_year_df.iterrows():
            base_df.loc[base_df['Country Code'] == row['Country Code'], 'GDP Deflator'] = row['GDP Deflator']

    # Create the map using the base_df instead of filtered data
    world_map = go.Figure(data=go.Choropleth(
        locations=base_df['Country Code'],
        z=base_df['GDP Deflator'],
        text=base_df['Country Name'],
        colorscale='RdBu',
        zmid=0,
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title="GDP Deflator (%)"
    ))

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
While the GDP deflator provides insights into how an economy is performing as a whole, it tells us nothing about how resources are distributed within that economy - this is why we turn to measures of inequality like the Gini coefficient.

The **Gini coefficient** is a measure of statistical dispersion intended to represent
the income inequality or wealth inequality within a nation or a social group.
It is the most commonly used measure of inequality. A Gini coefficient of 0
represents perfect equality, where everyone has the same income, while a Gini
coefficient of 1 implies perfect inequality, where one person has all the income
and everyone else has none. Most countries have Gini coefficients between 0.25-0.60, 
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

## Limitations of the Gini Coefficient

- **Lack of Detail on Sources of Inequality**: Does not identify whether inequality stems from wages, wealth, education, or other factors.
- **Insensitive to Distributional Extremes**: Struggles to capture changes at the very top or bottom of the income spectrum.
- **Ignores Population Structure**: Does not account for demographic differences like age or household composition.
- **No Clear Threshold**: Does not define what constitutes "acceptable" inequality levels.
- **Static View**: Represents inequality at a single point in time, ignoring income mobility over time.
- **Data Dependency**: Results are influenced by the accuracy and completeness of income or wealth data.
- **Focus on Monetary Metrics**: Excludes non-monetary dimensions like health, education, or access to resources.
- **Disregards Absolute Well-being**: Two regions with the same Gini coefficient may have vastly different living standards due to differences in average income.

This dashboard reads Gini coefficient data from a CSV file obtained from the [World Bank Open Data](https://data.worldbank.org/),
which contains Gini Indexes for various countries over a range of years. The Gini index is the Gini coefficient expressed as a percentage, and is equal to the Gini coefficient multiplied by 100.

                """)

    st.subheader("Data: ")
    st.write(gini_df)

    min_value = gini_df['Year'].min()
    max_value = gini_df['Year'].max()

    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_value,
        max_value=max_value,
        value=[2011, 2016] if min_value <= 2011 <= max_value and min_value <= 2016 <= max_value else [min_value, max_value])

    countries = gini_df['Country Name'].unique()

    if not len(countries):
        st.warning("Select at least one country")

    selected_countries = st.multiselect(
        'Which countries would you like to view?',
        countries,
        ['Germany', 'Brazil', 'Norway', 'United States', 'Estonia'])

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
    The metrics below display the Gini coefficients for the selected countries in the chosen final year. Under the Gini values, the number in green shows the change from the first year in the selected range, indicating whether inequality (as measured by Gini) has increased or decreased.
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
                label=f'{country} Gini',
                value=display_gini,
                delta=growth,
                delta_color=delta_color
            )

    # Poverty Section
    st.header('Poverty Headcount Ratio', divider='gray')

    poverty_df = get_poverty_data()

    # Poverty Headcount Ratio Dataset Information
    st.markdown("""
    #### About Poverty Headcount Ratio Data
    - **Source**: World Bank, Poverty and Inequality Platform.
    - **Indicator**: Poverty headcount ratio at $2.15 a day [(2017 PPP)](https://blogs.worldbank.org/en/opendata/how-do-2017-ppps-change-our-understanding-global-and-regional-poverty).
    - **Description**: Data are based on primary household survey data obtained from government statistical agencies and World Bank country departments. High-income economies' data are primarily from the Luxembourg Income Study database. More info at [pip.worldbank.org](https://pip.worldbank.org).

    #### Why is the Poverty Headcount Ratio Important?
    The **Poverty Headcount Ratio** is a critical measure of inequality that captures aspects of economic disparity that the Gini coefficient and GDP Deflator do not. While the Gini coefficient provides a broad measure of income inequality and the GDP Deflator reflects inflationary pressures, the Poverty Headcount Ratio directly measures the proportion of a population living below the poverty line, offering a more tangible and human-centric view of economic hardship.

    - **Human Impact**: Unlike the Gini coefficient, which can sometimes obscure the real-life implications of inequality, the Poverty Headcount Ratio highlights the actual number of people struggling to meet basic needs.
    - **Economic Development**: The GDP Deflator measures price changes in an economy, but it does not account for how these changes affect the poorest segments of society. The Poverty Headcount Ratio provides insight into whether economic growth is inclusive and benefits the most vulnerable populations.
    - **Policy Relevance**: Policymakers can use the Poverty Headcount Ratio to design targeted interventions aimed at poverty reduction, ensuring that economic policies are inclusive and equitable.

    #### Limitations of the Poverty Headcount Ratio
    - **Simplistic Threshold**: Focuses only on those below the poverty line, ignoring people just above it who may still face significant hardships.
    - **Ignores Depth of Poverty**: Does not capture how far below the poverty line individuals are, missing the severity of poverty for the most deprived.
    - **Static Measure**: Provides a snapshot of poverty at one point in time, failing to reflect changes in individual or household circumstances over time.
    - **Relies on Arbitrary Thresholds**: The poverty line ($2.15 a day, 2017 PPP) may not account for regional cost-of-living differences or varying definitions of basic needs.
    - **Limited Multidimensional Insights**: Focuses solely on income, overlooking other aspects of poverty like access to healthcare, education, or housing.
    - **Data Quality and Comparability**: Dependent on the accuracy of household surveys and consistency across countries, which can vary significantly.

    This metric is essential for understanding the breadth of poverty within a country, making it a vital tool for assessing the effectiveness of poverty alleviation programs and economic policies.
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
    ### Understanding Income Distribution through Quintile Shares

    The **quintile shares** indicate how total income is distributed across five equal segments (20% each) of the population, ordered from lowest to highest income. This metric provides a detailed view of income inequality that complements both the Gini coefficient and Poverty Headcount Ratio.

    #### Data Source
    The data presented here is sourced from the [World Income Inequality Database (WIID)](https://www.wider.unu.edu/database/world-income-inequality-database-wiid) by UNU-WIDER.

    #### What are Quintile Shares?
    - The population is divided into five equal groups (quintiles) based on income.
    - First quintile (Q1): Poorest 20% of the population.
    - Fifth quintile (Q5): Richest 20% of the population.
    - Shares are expressed as percentages of total income.

    #### Advantages over Other Inequality Measures:
    - **More Granular than Gini**: While the Gini coefficient provides a single number, quintile shares show exactly where in the distribution inequality occurs.
    - **More detailed than Poverty Headcount**: Instead of just showing how many are below a threshold, quintiles reveal the entire distribution of income.
    - **Policy Relevance**: Offers a detailed view of income or wealth distribution across different segments of society, enabling the design of more effective redistributive policies.

    #### Reading the Visualization:
    - Each bar represents 100% of a country's income.
    - The five colored segments show how that income is divided.
    - In a perfectly equal society, each quintile would receive 20% of total income.
    - Larger top quintile shares indicate greater inequality.

    Note: If your selected country doesn't appear in the plot, data for that country-year combination is not available in the WIID.
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
        ).groupby(['country', 'Quintile'], as_index=False).sum()

        # Create more readable quintile labels
        melted_wiid_df['Quintile'] = pd.Categorical(
            melted_wiid_df['Quintile'].map({
                'q1': '0-20%',
                'q2': '20-40%',
                'q3': '40-60%',
                'q4': '60-80%',
                'q5': '80-100%'
            }),
            categories=['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
            ordered=True
        )

        # Create the Altair chart with stacked bars
        quintile_chart = alt.Chart(melted_wiid_df).mark_bar().encode(
            x=alt.X('country:N', title='Country'),
            y=alt.Y(
                'Income Share:Q',
                title='Income Share (%)',
                stack='normalize',
                axis=alt.Axis(format='.1f')
            ),
            color=alt.Color(
                'Quintile:N',
                title='Quintile',
                scale=alt.Scale(scheme='spectral'),
                sort=['Top 20%', 'Middle (upper) 20%', 'Middle 20%', 'Middle (lower) 20%', 'Bottom 20%']
            ),
            order=alt.Order('Quintile:N', sort='ascending'),
            tooltip=[
                alt.Tooltip('country:N', title='Country'),
                alt.Tooltip('Quintile:N', title='Quintile')
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
        # Add Palma ratio and other inequality metrics over time
        st.header('Income Inequality Ratios', divider='gray')
        st.markdown("""
        ### Understanding Alternative Inequality Metrics: Ratios

        In the previous section, we explored income distribution through quintile shares, which provided a detailed view of how income is distributed across different segments of the population. Building on that, we can derive additional insights using specific ratios that highlight different aspects of inequality.

        - **Palma Ratio**: The ratio of the richest 10%'s share of gross national income divided by the poorest 40%'s share. This metric emphasizes the disparity between the top and bottom of the income distribution.
        - **Top20/Bottom20 Ratio**: The ratio of income share of the richest 20% to the poorest 20%. This ratio is directly derived from the quintile data explored above and provides a clear measure of inequality between the top and bottom quintiles.
        - **Upper Middle/Lower Middle Ratio**: The ratio of income share between the upper middle (Q4) and lower middle (Q2) quintiles. This ratio, also derived from the quintile data, highlights the disparity within the middle segments of the population.

        These ratios offer a more detailed understanding of income inequality, complementing the quintile shares by focusing on specific parts of the income distribution and the relationship between them. These ratios are also helpful for analyzing relative changes in inequality across time.
        """)

        # Country selector for metrics
        metric_countries = sorted(wiid_df['country'].unique())
        selected_metric_country = st.selectbox(
            'Select a country for inequality metrics',
            options=metric_countries,
            index=metric_countries.index('Estonia') if 'Estonia' in metric_countries else 0
        )

        # Filter available years for the selected country
        available_years_for_country = sorted(wiid_df[wiid_df['country'] == selected_metric_country]['year'].unique())
        
        # Time range selector for metrics
        default_min_year = 2005 if 2005 in available_years_for_country else min(available_years_for_country)
        default_max_year = 2021 if 2021 in available_years_for_country else max(available_years_for_country)
        
        metric_min_year, metric_max_year = st.slider(
            'Select time range for inequality metrics',
            min_value=int(min(available_years_for_country)),
            max_value=int(max(available_years_for_country)),
            value=[int(default_min_year), int(default_max_year)]
        )

        if metric_countries:
            # Filter data for selected country and years
            metrics_df = wiid_df[
            (wiid_df['country'] == selected_metric_country) &
            (wiid_df['year'] >= metric_min_year) &
            (wiid_df['year'] <= metric_max_year)
            ].copy()

            # Ensure only one value per country per year
            metrics_df = metrics_df.drop_duplicates(subset=['country', 'year'])

            # Calculate upper middle to lower middle ratio
            metrics_df['upper_middle_to_lower'] = metrics_df['q4'] / metrics_df['q2']

            # Prepare data for plotting
            metrics_long = pd.melt(
            metrics_df,
            id_vars=['country', 'year'],
            value_vars=['palma', 'ratio_top20bottom20', 'upper_middle_to_lower'],
            var_name='metric',
            value_name='value'
            )

            # Create nicer labels for metrics
            metrics_long['metric'] = metrics_long['metric'].map({
            'palma': 'Palma Ratio',
            'ratio_top20bottom20': 'Top20/Bottom20 Ratio',
            'upper_middle_to_lower': 'Upper/Lower Middle Ratio'
            })

        # Add ratio selector
        selected_ratios = st.multiselect(
            'Select ratios to display',
            ['Palma Ratio', 'Top20/Bottom20 Ratio', 'Upper/Lower Middle Ratio'],
            ['Palma Ratio', 'Top20/Bottom20 Ratio', 'Upper/Lower Middle Ratio']
        )

        if not selected_ratios:
            st.warning("Please select at least one ratio to display.")
        else:
            # Filter for selected ratios
            metrics_long = metrics_long[metrics_long['metric'].isin(selected_ratios)]

            # Create the chart with lines connecting consecutive years
            metrics_chart = alt.Chart(metrics_long).mark_line(
            point=True,
            strokeWidth=2
            ).encode(
            x=alt.X('year:O', 
                title='Year',
                axis=alt.Axis(labelAngle=0)
            ),
            y=alt.Y('value:Q', 
                title='Ratio Value',
                scale=alt.Scale(zero=False)
            ),
            color=alt.Color('metric:N', 
                title='Ratio Type',
                legend=alt.Legend(
                orient='top',
                titleFontSize=12,
                labelFontSize=11
                )
            ),
            tooltip=['country:N', 'year:O', 'metric:N', 
                alt.Tooltip('value:Q', format='.2f')]
            ).properties(
            title=f'Inequality Metrics Over Time for {selected_metric_country}',
            height=400
            ).interactive()

            st.altair_chart(metrics_chart, use_container_width=True)
            # Closing Section
            st.header('Thank you!', divider='gray')
            st.markdown("""
            ### Thank You for Exploring the Inequality Dashboard

            We hope the visualizations and data provided some insights into various aspects of economic inequality across different countries and time periods.

            **Reminder**: Feel free to save the data visualizations you created by clicking on the three dots in the top right corner of the plots and selecting the desired format.

            For more detailed information and personalized assistance, check out our **Chatbot** feature at the top. The Chatbot can help answer your questions and provide additional information on inequality metrics, economic indicators, and more.
            """)
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

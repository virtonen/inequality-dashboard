import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path

from navigation.about_project import show_about_project
from navigation.about_us import show_about_us
from navigation.who_is_this_for import show_who_is_this_for

# Set the page configuration
st.set_page_config(
    page_title="World Inequality Dashboard",
    page_icon=":earth_americas:",
)

# Title at the top of the app
st.markdown(
    "<h1 style='text-align: center;'>🌎 World Inequality Dashboard</h1>", 
    unsafe_allow_html=True
)

# Navigation buttons with unique keys
def show_navigation_buttons():
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🏠 Home", key="home_btn"):
        st.session_state.page = "Home"
    if col2.button("🔍 About Project", key="about_project_btn"):
        st.session_state.page = "About Project"
    if col3.button("📖 About Us", key="about_us_btn"):
        st.session_state.page = "About Us"
    if col4.button("👥 Who is This For?", key="who_is_this_for_btn"):
        st.session_state.page = "Who is This For?"

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Show navigation buttons at the top
show_navigation_buttons()

# Page Navigation Logic
if st.session_state.page == "Home":
    # Render Home Page Content
    st.markdown("""
    ### Welcome!  
    Explore the dashboard to learn about **GDP Trends**, **Gini Coefficient**, and **Poverty Ratios**.
    """)

    st.markdown("""
    ## Table of Contents
    - [GDP Comparison](#gdp-comparison)
    - [Gini Coefficient](#gini-coefficient)
    - [Poverty Headcount Ratio](#poverty-headcount-ratio-over-time)
    """)
        # Data Sections: GDP, Gini, and Poverty Ratio
    st.header('GDP Comparison', divider='gray')
    st.markdown("Some insights about GDP data")
    st.write("**[Insert GDP Comparison Data and Chart here.]**")

    st.header('Gini Coefficient', divider='gray')
    st.markdown("Some insights about Gini Coefficient data")
    st.write("**[Insert Gini Coefficient Data and Chart here.]**")

    st.header('Poverty Headcount Ratio', divider='gray')
    st.markdown("Some insights about Poverty Headcount Ratio data")
    st.write("**[Insert Poverty Headcount Ratio Data and Chart here.]**")

elif st.session_state.page == "About Project":
    # Call About Project Page Content
    show_about_project()

elif st.session_state.page == "About Us":
    # Call About Us Page Content
    show_about_us()

elif st.session_state.page == "Who is This For?":
    # Call Who is This For Page Content
    show_who_is_this_for()

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
st.markdown(r"""
## Gini Coefficient

The **Gini coefficient** is a measure of statistical dispersion intended to represent
the income inequality or wealth inequality within a nation or a social group.
It is the most commonly used measure of inequality. A Gini coefficient of 0
represents perfect equality, where everyone has the same income, while a Gini
coefficient of 100 implies perfect inequality, where one person has all the income
and everyone else has none. Most countries have Gini coefficients between 25-60, with lower values indicating more equality and higher values indicating more inequality.

## Relation to the Lorenz Curve
The Gini coefficient is derived from the [Lorenz curve](https://en.wikipedia.org/wiki/Lorenz_curve),
which graphically represents the distribution of income or wealth within a population.
The Gini coefficient is defined as the ratio of the area between the Lorenz curve and the line of equality
to the total area under the line of equality. This gives a numerical value that summarizes the degree of income inequality.

## Limitations of the Gini Coefficient
While the Gini coefficient is a powerful tool for measuring inequality, it is not without its limitations. Understanding these limitations is important for interpreting the data accurately and comprehensively:
- **Absolute Wealth or Income Levels**: It does not account for the overall level of income or wealth in a country. Two countries with vastly different economic conditions can have the same Gini coefficient, despite significant differences in living standards.
- **Population Size**: It also does not consider the size of a population. Larger populations with diverse demographics might require additional metrics to fully capture inequality.
- **Regional Disparities**: It represents inequality at a national level but does not reflect disparities within regions or communities. For example, rural and urban areas might have vastly different income distributions.

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

The Gini coefficient gives a succinct, easy-to-understand metric for comparing levels of income inequality between different countries or time periods. It's an important tool for economists, policymakers, and the public to assess the fairness and distribution of economic resources within a society.
This dashboard sources Gini coefficient data from the [World Bank Open Data](https://data.worldbank.org/), which compiles this statistic for many countries over multiple years. The data allows users to easily visualize and compare income inequality levels around the world.
""")

# Add some spacing
''
''

# data 
st.subheader("Data: ")
st.write(gini_df)

# null values 
st.subheader("Null values: ")
st.write(null_perc(gini_df) )

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

''
''
''

# Filter the data
filtered_gini_df = gini_df[
    (gini_df['Country Name'].isin(selected_countries))
    & (gini_df['Year'] <= to_year)
    & (from_year <= gini_df['Year'])
]

st.header('Gini over time', divider='gray')

''

gini_chart = alt.Chart(filtered_gini_df).mark_line().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),  # No commas in Year
    y=alt.Y('GINI', title='GINI'),
    color='Country Name:N',  # Use Country Name for legend
    tooltip=['Country Name', 'Year', 'GINI']
).properties(
    title='Gini Coefficient over Time'
)

st.altair_chart(gini_chart, use_container_width=True)

''
''

first_year = gini_df[gini_df['Year'] == from_year]
last_year = gini_df[gini_df['Year'] == to_year]

st.header(f'Gini in {to_year}', divider='gray')

''

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


# -----------------------------------------------------------------------------

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

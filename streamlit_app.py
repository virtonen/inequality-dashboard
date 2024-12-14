import streamlit as st
import pandas as pd
import math
import altair as alt
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='World Inequality Dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

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

# Set the title that appears at the top of the page.
st.markdown(r"""
# :earth_americas: World Inequality Dashboard
            
## Gini Coefficient

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
    ['Germany', 'Brazil', 'Norway', 'South Africa', 'Australia', 'China'])

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

st.line_chart(
    filtered_gini_df,
    x='Year',
    y='GINI',
    color='Country Name',
)

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
""")

# Filter years and countries for poverty data
poverty_min_year = poverty_df['Year'].min()
poverty_max_year = poverty_df['Year'].max()

poverty_from_year, poverty_to_year = st.slider(
    'Which years are you interested in for poverty data?',
    min_value=poverty_min_year,
    max_value=poverty_max_year,
    value=[poverty_min_year, poverty_max_year]
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

# -----------------------------------------------------------------------------

st.header('GDP Comparison', divider='gray')

st.markdown("""
Some insigths about GDP data""")

# GDP DATA
def get_gdp_deflator_data():
    """Grab GDP deflator data from the world_bank_popular_indicators dataset."""
    DATA_FILENAME = Path(__file__).parent/'data/world_bank_popular_indicators.csv'
    raw_gdp_deflator_df = pd.read_csv(DATA_FILENAME)

    #MIN_YEAR = 2000
    #MAX_YEAR = 2015

    # Filter the dataset for the specific Series Code
    gdp_deflator_df = raw_gdp_deflator_df[raw_gdp_deflator_df['Series Code'] == 'NY.GDP.DEFL.KD.ZG']

    # Melt the dataset into long format
    gdp_deflator_df = gdp_deflator_df.melt(
        id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
        var_name='Year',
        value_name='GDP Deflator'
    )

    # Convert Year to numeric and drop rows with missing GDP Deflator values
    gdp_deflator_df['Year'] = gdp_deflator_df['Year'].str.extract('(\d{4})').astype(float)
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

#gdp_from_year, gdp_to_year = st.slider(
#    'Which years are you interested in for GDP deflator data?',
#    min_value=gdp_min_year,
#    max_value=gdp_max_year,
#    value=[gdp_min_year, gdp_max_year]
#)
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
    ['United States', 'China', 'India']  # Add any defaults you prefer
)

# Filter the GDP Deflator Data
filtered_gdp_deflator_df = gdp_deflator_df[
    (gdp_deflator_df['Country Name'].isin(selected_gdp_countries))
    & (gdp_deflator_df['Year'] <= gdp_to_year)
    & (gdp_deflator_df['Year'] >= gdp_from_year)
]


gdp_deflator_chart = alt.Chart(filtered_gdp_deflator_df).mark_line().encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('GDP Deflator:Q',  # Treat GDP Deflator as quantitative
            title='GDP Deflator (%)',
            axis=alt.Axis(format='.2f')),  # Ensure numerical formatting
    color='Country Name:N',
    tooltip=['Country Name', 'Year', 'GDP Deflator']
).properties(
    title='GDP Deflator over time'
)
st.altair_chart(gdp_deflator_chart, use_container_width=True)

# -----------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the GDP deflator data
gdp_deflator_df = filtered_gdp_deflator_df  # Ensure this is already pre-filtered as needed

# Get the unique years and countries in the data
years = gdp_deflator_df['Year'].unique()
countries = sorted(gdp_deflator_df['Country Name'].unique())  # Sort countries alphabetically for clarity

# Allow the user to select the year
selected_year = st.slider(
    'Select the year',
    min_value=int(years.min()),
    max_value=int(years.max()),
    value=int(years.max())
)

# Checkbox to select all or none of the countries
select_all = st.checkbox('Select all countries', value=False)

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
world_map = go.Figure(data=go.Choropleth(
    locations=gdp_deflator_year_df['Country Code'],
    z=gdp_deflator_year_df['GDP Deflator'],
    text=gdp_deflator_year_df['Country Name'],  # Add country name to tooltips
    colorscale='Viridis',
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
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: World Inequality Database',
        showarrow=False
    )]
)

# Display the map in the Streamlit app
st.plotly_chart(world_map, use_container_width=True)

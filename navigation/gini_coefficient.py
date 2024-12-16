import streamlit as st
import pandas as pd
import altair as alt
import math
from pathlib import Path

# Define function to load Gini data
@st.cache_data
def get_gini_data():
    """Load and process Gini data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent / 'data/gini_data.csv'
    raw_gini_df = pd.read_csv(DATA_FILENAME)
    gini_df = raw_gini_df.melt(
        ['Country Name', 'Country Code'],
        var_name='Year',
        value_name='GINI'
    )
    gini_df['Year'] = pd.to_numeric(gini_df['Year'])
    return gini_df

# Load Gini data
gini_df = get_gini_data()

# Define a function to calculate null percentages
def null_perc(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    return missing_value_df

# Page Content
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

# Display data
st.subheader("Data: ")
st.write(gini_df)

# Display null values
st.subheader("Null values: ")
st.write(null_perc(gini_df))

# Slider for year range
min_value = gini_df['Year'].min()
max_value = gini_df['Year'].max()
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
gini_chart = alt.Chart(filtered_gini_df).mark_line().encode(
    x=alt.X('Year:O', title='Year', axis=alt.Axis(format='d')),  # No commas in Year
    y=alt.Y('GINI', title='GINI'),
    color='Country Name:N',  # Use Country Name for legend
    tooltip=['Country Name', 'Year', 'GINI']
).properties(
    title='Gini Coefficient over Time'
)
st.altair_chart(gini_chart, use_container_width=True)

# Display metrics
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
        first_gini = first_year[first_year['Country Name'] == country]['GINI'].iat[0] if not first_year[first_year['Country Name'] == country].empty else None
        last_gini = last_year[last_year['Country Name'] == country]['GINI'].iat[0] if not last_year[last_year['Country Name'] == country].empty else None
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

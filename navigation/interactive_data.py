import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
import math

# Cache decorators for each data loading function
@st.cache_data
def get_gdp_data():
    """Load and process GDP data"""
    DATA_FILENAME = Path(__file__).parent.parent/'data/world_bank_popular_indicators.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    return raw_gdp_df

@st.cache_data
def get_gini_data():
    """Grab GINI data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent.parent/'data/gini_data.csv'
    raw_gini_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2023

    # Pivot year columns into rows
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

    # Convert Year to numeric and drop rows with missing values
    poverty_df['Year'] = pd.to_numeric(poverty_df['Year'], errors='coerce')
    poverty_df = poverty_df.dropna(subset=['Poverty Headcount Ratio'])
    
    return poverty_df

def null_perc(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    return missing_value_df

def show_Interactive_Data():
    # 1. GDP Section
    st.header('GDP Comparison', divider='gray')
    st.markdown("""Some insights about GDP data""")
    
    # Load GDP data
    gdp_df = get_gdp_data()
    gdp_deflator_df = gdp_df[gdp_df['Series Code'] == 'NY.GDP.DEFL.KD.ZG'].copy()
    
    # GDP year range selection
    gdp_years = [int(col[-4:]) for col in gdp_df.columns if 'YR' in col]
    gdp_min_year, gdp_max_year = min(gdp_years), max(gdp_years)
    
    gdp_from_year, gdp_to_year = st.slider(
        'Which years are you interested in for GDP deflator data?',
        min_value=gdp_min_year,
        max_value=gdp_max_year,
        value=[gdp_min_year, gdp_max_year]
    )

    # GDP country selection
    gdp_countries = gdp_deflator_df['Country Name'].unique()
    selected_gdp_countries = st.multiselect(
        'Which countries would you like to view for GDP deflator data?',
        gdp_countries,
        ['United States', 'China', 'India']
    )

    # Create GDP visualization
    if selected_gdp_countries:
        # Prepare GDP data
        gdp_data = gdp_deflator_df.melt(
            id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
            value_vars=[f'YR{year}' for year in range(gdp_from_year, gdp_to_year + 1)],
            var_name='Year',
            value_name='GDP Deflator'
        )
        gdp_data['Year'] = gdp_data['Year'].str[-4:].astype(int)
        
        filtered_gdp = gdp_data[
            (gdp_data['Country Name'].isin(selected_gdp_countries)) &
            (gdp_data['Year'].between(gdp_from_year, gdp_to_year))
        ]

        gdp_chart = alt.Chart(filtered_gdp).mark_line().encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('GDP Deflator:Q', title='GDP Deflator (%)'),
            color='Country Name:N',
            tooltip=['Country Name', 'Year', 'GDP Deflator']
        ).properties(
            title='GDP Deflator over time'
        )
        
        st.altair_chart(gdp_chart, use_container_width=True)

    # 2. Gini Coefficient Section
    st.header('Gini Coefficient Analysis', divider='gray')
    
    # Load Gini data
    gini_df = get_gini_data()
    
    # Display data and null values
    st.subheader("Data Overview:")
    st.write(gini_df)
    
    st.subheader("Missing Values Analysis:")
    st.write(null_perc(gini_df))
    
    # Gini year range selection
    gini_min_year = gini_df['Year'].min()
    gini_max_year = gini_df['Year'].max()
    
    gini_from_year, gini_to_year = st.slider(
        'Select years for Gini analysis:',
        min_value=gini_min_year,
        max_value=gini_max_year,
        value=[gini_min_year, gini_max_year]
    )
    
    # Gini country selection
    gini_countries = gini_df['Country Name'].unique()
    selected_gini_countries = st.multiselect(
        'Select countries for Gini analysis:',
        gini_countries,
        ['Germany', 'Brazil', 'Norway', 'South Africa', 'United States', 'Estonia']
    )

    if selected_gini_countries:
        # Filter Gini data
        filtered_gini = gini_df[
            (gini_df['Country Name'].isin(selected_gini_countries)) &
            (gini_df['Year'].between(gini_from_year, gini_to_year))
        ]

        # Create Gini visualization
        gini_chart = alt.Chart(filtered_gini).mark_line().encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('GINI:Q', title='GINI Coefficient'),
            color='Country Name:N',
            tooltip=['Country Name', 'Year', 'GINI']
        ).properties(
            title='Gini Coefficient over Time'
        )
        
        st.altair_chart(gini_chart, use_container_width=True)

        # Show Gini metrics
        st.header(f'Gini Comparison {gini_to_year}', divider='gray')
        
        first_year = gini_df[gini_df['Year'] == gini_from_year]
        last_year = gini_df[gini_df['Year'] == gini_to_year]
        
        cols = st.columns(4)
        for i, country in enumerate(selected_gini_countries):
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

    # 3. Poverty Section
    st.header('Poverty Analysis', divider='gray')
    
    # Load poverty data
    poverty_df = get_poverty_data()
    
    # Poverty year range selection
    poverty_min_year = poverty_df['Year'].min()
    poverty_max_year = poverty_df['Year'].max()
    
    poverty_from_year, poverty_to_year = st.slider(
        'Select years for poverty analysis:',
        min_value=int(poverty_min_year),
        max_value=int(poverty_max_year),
        value=[int(poverty_min_year), int(poverty_max_year)]
    )
    
    # Poverty country selection
    poverty_countries = poverty_df['Country Name'].unique()
    selected_poverty_countries = st.multiselect(
        'Select countries for poverty analysis:',
        poverty_countries,
        ['Argentina', 'Chile', 'Ethiopia']
    )

    if selected_poverty_countries:
        # Filter poverty data
        filtered_poverty = poverty_df[
            (poverty_df['Country Name'].isin(selected_poverty_countries)) &
            (poverty_df['Year'].between(poverty_from_year, poverty_to_year))
        ]

        # Create poverty visualization
        poverty_chart = alt.Chart(filtered_poverty).mark_line().encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('Poverty Headcount Ratio:Q', title='Headcount Ratio (%)'),
            color='Country Name:N',
            tooltip=['Country Name', 'Year', 'Poverty Headcount Ratio']
        ).properties(
            title='Poverty Headcount Ratio at $2.15/day (2017 PPP)'
        )
        
        st.altair_chart(poverty_chart, use_container_width=True)

if __name__ == "__main__":
    show_Interactive_Data()

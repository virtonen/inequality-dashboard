import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

@st.cache_data
def get_gdp_data():
    """Load and process GDP data"""
    DATA_FILENAME = Path(__file__).parent.parent/'data/world_bank_popular_indicators.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    
    # Filter for GDP series
    gdp_df = raw_gdp_df[raw_gdp_df['Series Code'] == 'NY.GDP.DEFL.KD.ZG']
    
    return gdp_df

def show_interactive_data():
    st.header('Interactive Data Analysis', divider='gray')
    
    # Load data
    try:
        gdp_df = get_gdp_data()
        
        # Get year columns
        year_cols = [col for col in gdp_df.columns if 'YR' in col]
        
        # Melt the dataframe
        gdp_long = gdp_df.melt(
            id_vars=['Country Name', 'Country Code', 'Series Name', 'Series Code'],
            value_vars=year_cols,
            var_name='Year',
            value_name='Value'
        )
        
        # Convert Year to numeric
        gdp_long['Year'] = gdp_long['Year'].str.extract('(\d{4})').astype(int)
        
        # User inputs
        st.subheader('GDP Deflator Analysis')
        
        # Country selection
        countries = sorted(gdp_long['Country Name'].unique())
        selected_countries = st.multiselect(
            'Select countries to compare:',
            countries,
            default=['United States', 'China', 'India']
        )
        
        # Year range selection
        min_year = gdp_long['Year'].min()
        max_year = gdp_long['Year'].max()
        year_range = st.slider(
            'Select year range:',
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # Filter data based on selection
        filtered_data = gdp_long[
            (gdp_long['Country Name'].isin(selected_countries)) &
            (gdp_long['Year'].between(year_range[0], year_range[1]))
        ]
        
        # Create chart
        if not filtered_data.empty:
            chart = alt.Chart(filtered_data).mark_line().encode(
                x=alt.X('Year:O', title='Year'),
                y=alt.Y('Value:Q', title='GDP Deflator (%)'),
                color='Country Name:N',
                tooltip=['Country Name', 'Year', 'Value']
            ).properties(
                title='GDP Deflator Trends',
                width=700,
                height=400
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Show data table
            st.subheader('Data Table')
            st.dataframe(filtered_data.sort_values(['Country Name', 'Year']))
        else:
            st.warning('Please select at least one country to display the data.')
            
    except Exception as e:
        st.error(f'Error loading or processing data: {str(e)}')
        st.write('Please check if the data file exists and is accessible.')

if __name__ == "__main__":
    show_interactive_data()

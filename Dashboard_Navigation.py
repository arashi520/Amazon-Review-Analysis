import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_plotly_events import plotly_events

#######################################
# PAGE SETUP
#######################################
def load_css(css_file):
    """Load the CSS file"""
    with open(css_file, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_data(path):
    data = pd.read_csv(path, usecols=['latitude', 'longitude', 'abbreviatedAddress', 'subdivisionName', 'datePostedString', 'dateSoldString', 'price', 'description'])
    # Convert date columns to datetime
    data['datePostedString'] = pd.to_datetime(data['datePostedString'], errors='coerce')
    data['dateSoldString'] = pd.to_datetime(data['dateSoldString'], errors='coerce')
    return data

def map(data, neighborhood, date_range):
    # Filter by neighborhood
    if neighborhood != "All":
        data = data[data['subdivisionName'] == neighborhood]
    
    # Convert date_range to datetime64[ns]
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    
    # Filter by date range
    data = data[(data['dateSoldString'] >= start_date) & (data['dateSoldString'] <= end_date)]
    
    # Map
    seattle_data = data.dropna(subset=['latitude', 'longitude'])
    
    # Calculate median latitude and longitude for initial map center
    median_lat = seattle_data['latitude'].median()
    median_lon = seattle_data['longitude'].median()

    # Create a map using Plotly
    fig = px.scatter_mapbox(
        seattle_data,
        lat="latitude",
        lon="longitude",
        hover_name="abbreviatedAddress",
        hover_data={
            "latitude": False,
            "longitude": False,
            "abbreviatedAddress": True,
            "subdivisionName": True,
            "datePostedString": False,
            "dateSoldString": False,
            "price": True,
            "description": False
        },
        color_discrete_sequence=["fuchsia"],
        zoom=10,
        height=600,
        center={"lat": median_lat, "lon": median_lon}
    )

    # Customize the layout of the map
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(
        marker=dict(
            color='#4169E1',  
            size=6,         
            # symbol='circle'  
        )
    )

    # Display the map in Streamlit
    selected_points = plotly_events(fig, click_event=True, hover_event=False, override_height=600, override_width="100%")

    if selected_points:
        selected_index = selected_points[0]["pointIndex"]
        st.session_state['selected_property'] = seattle_data.iloc[selected_index]

    if 'selected_property' in st.session_state:
        display_property_details(st.session_state['selected_property'])

def display_property_details(details):
    st.write("### Property Details")
    st.write(f"**Subdivision**: {details['subdivisionName']}")
    st.write(f"**Address**: {details['abbreviatedAddress']}")
    st.write(f"**Posted Date**: {details['datePostedString']}")
    st.write(f"**Sold Date**: {details['dateSoldString']}")
    st.write(f"**Sold Price**: ${details['price']}")
    st.write(f"**Description**: {details['description']}")

def main():
    # Configure page settings
    st.set_page_config(
        page_title="Seattle Housing Market Dashboard",
        page_icon="🏠",
        layout="wide"
    )

    st.title("Seattle Housing Market: Sold House Analysis")

    # Load the CSS file
    load_css("asset/style.css")
    
    # Load data
    data = load_data("data/long_listing.csv")

    # Header
    st.markdown("""
        <div class="header-container">
            <header class="header-text">Wayber@Seattle: proptotype dashboard for testing purpose</header>
        </div>
    """, unsafe_allow_html=True)

    # Content
    st.markdown("""
        <div class="about-content-container">
            <h1 class="title"> Seattle Properties Sold in the Past Year </h1>
            <div class="summary">Welcome to our interactive visualization dashboard! This dynamic tool is designed to analyze the housing market in Seattle. 
            This platform is built upon comprehensive property data, providing deep insights and trends in a wide range of real estate metrics.</div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.markdown("# Wayber Inc. 🏠")

    # Sidebar filters
    st.sidebar.markdown("# Filters")
    
    neighborhoods = ["All"] + sorted(data['subdivisionName'].dropna().unique().tolist())
    selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", neighborhoods)

    min_date = data['dateSoldString'].min().date()
    max_date = data['dateSoldString'].max().date()
    date_range = st.sidebar.slider("Select Date Range", min_date, max_date, (min_date, max_date))

    # Show Map
    map(data, selected_neighborhood, date_range)



if __name__ == "__main__":
    main()

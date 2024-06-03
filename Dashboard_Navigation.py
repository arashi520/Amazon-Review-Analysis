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

def main():
    # Configure page settings
    st.set_page_config(
        page_title="Amazon Analysis",
        page_icon="🛍️",
        layout="wide"
    )

    st.title("Amazon All Beauty Category Reviews 2023")

    # Load the CSS file
    load_css("asset/style.css")
    
    # Load data
    # data = load_data("data/long_listing.csv")

    # Header
    st.markdown("""
        <div class="header-container">
            <header class="header-text">IMT 563 Advanced Database Management System @ Amazon All Beauty Category Reviews 2023 Data Visualization</header>
        </div>
    """, unsafe_allow_html=True)

    # Content
    st.markdown("""
        <div class="about-content-container">
            <h1 class="title"> Analysis of Amazon All Beauty Category Reviews from user, product, and review perspectives</h1>
            <div class="summary">Welcome to our interactive visualization dashboard! This dynamic tool is designed to analyze the Amazon Beauty Product Reviews. 
            This platform is built upon comprehensive item and review data, providing deep insights and trends in a wide range of eCommerce metrics.</div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    # st.sidebar.markdown("# IMT 563")

    # Sidebar filters
    # st.sidebar.markdown("# Filters")
    


if __name__ == "__main__":
    main()

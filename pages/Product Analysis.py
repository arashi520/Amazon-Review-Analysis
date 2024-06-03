import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def load_css(css_file):
    """Load the CSS file"""
    with open(css_file, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_data
def load_data(path):
    data = pd.read_json(path, lines=True, orient='records')
    data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
    data['rating_number'] = pd.to_numeric(data['rating_number'], errors='coerce')
    data['main_category'] = data['main_category'].astype(str)
    data['store'] = data['store'].astype(str)
    return data.copy()

def create_bar_chart(data):
    """Create a bar chart showing the number of ratings for the top ten stores"""
    data_cleaned = data[data['store'] != 'None']
    top_stores = data_cleaned['store'].value_counts().head(10)
    fig = px.bar(top_stores, x=top_stores.index, y=top_stores.values, labels={'x': 'Store', 'y': 'Number of Ratings'}, title='Top 10 Stores by Rating Number')
    fig.update_layout(xaxis_title='Store', yaxis_title='Number of Ratings', template='plotly_white', title_font_size=20, width=1000, height=500)
    fig.update_traces(marker_color='lightskyblue')
    return fig

def create_histogram(data):
    """Create a histogram showing the distribution of average ratings for products with rating number greater than 50"""
    filtered_data = data[data['rating_number'] > 50]
    fig = px.histogram(filtered_data, x='average_rating', title='Distribution of Average Rating for Products with Rating Number > 50')
    fig.update_layout(xaxis_title='Average Rating', yaxis_title='Count', template='plotly_white', title_font_size=20, width=500, height=500)
    fig.update_traces(marker_color='lightcoral')
    return fig

def create_wordcloud(data):
    """Create a word cloud of the top 100 product titles by rating number"""
    top_titles = data.sort_values('rating_number', ascending=False).head(100)['title']
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(top_titles))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def main():
    # Load data
    data = load_data("data/output_data_item.jsonl")

    # Set Streamlit page title
    st.title("Amazon Product Analysis")

    # Header
    st.markdown("""
        <div class="header-container" style="background-color: #f9f9f9; padding: 10px; border-radius: 5px;">
            <header class="header-text" style="font-size: 24px; font-weight: bold;">IMT 563 @ Amazon All Beauty Category Reviews 2023 Data Visualization</header>
        </div>
    """, unsafe_allow_html=True)

    # Create and display the histogram and word cloud side by side
    col1, col2 = st.columns(2)

    with col1:
        fig2 = create_histogram(data)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig1 = create_bar_chart(data)
        st.plotly_chart(fig1, use_container_width=True)

    # Create and display the bar chart
    st.write("### Word Cloud of Top 100 Titles by Rating Number")
    fig3 = create_wordcloud(data)
    st.pyplot(fig3, use_container_width=True)


# Call the main function
if __name__ == "__main__":
    main()

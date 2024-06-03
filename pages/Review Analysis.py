import streamlit as st
import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_css(css_file):
    """Load the CSS file"""
    with open(css_file, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_data(filepath):
    """Load data from a JSONL file"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def plot_rating_distribution(df):
    """Plot rating distribution"""
    st.subheader("Review Ratings Distribution")
    rating_counts = df['rating'].value_counts().sort_index()
    st.bar_chart(rating_counts, use_container_width=True)

def plot_helpful_vote_distribution(df):
    """Plot helpful vote distribution"""
    st.subheader("Helpful Vote Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df['helpful_vote'], bins=100, color='skyblue', edgecolor='black')
    ax.set_xlabel('Helpful Votes')
    ax.set_ylabel('Number of Reviews')
    ax.set_title('Distribution of Helpful Votes')
    st.pyplot(fig, use_container_width=True)

def display_top_helpful_reviews(df):
    """Display top 10 reviews with most helpful votes"""
    st.subheader("Top 10 Reviews with Most Helpful Votes")
    top_10_helpful_reviews = df.nlargest(10, 'helpful_vote')[['user_id', 'rating', 'text', 'helpful_vote']]
    st.write(top_10_helpful_reviews)

def plot_wordcloud(df):
    """Plot word cloud of review text"""
    st.subheader("Word Cloud of Review Text")
    text = " ".join(review for review in df['text'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)

def main():
    # Load data
    data_filepath = 'data/output_data_review.jsonl'
    df = load_data(data_filepath)

    # Set Streamlit page title
    st.title("Amazon Review Analysis")

    # Header
    st.markdown("""
        <div class="header-container" style="background-color: #f9f9f9; padding: 10px; border-radius: 5px;">
            <header class="header-text" style="font-size: 24px; font-weight: bold;">IMT 563 @ Amazon All Beauty Category Reviews 2023 Data Visualization</header>
        </div>
    """, unsafe_allow_html=True)

    # Display plots in two columns and two rows format
    col1, col2 = st.columns(2)

    with col1:
        plot_rating_distribution(df)
        plot_wordcloud(df)
    
    with col2:
        plot_helpful_vote_distribution(df)
        display_top_helpful_reviews(df)

# Load custom CSS (optional)
# load_css('style.css')

# Run main function
if __name__ == "__main__":
    main()

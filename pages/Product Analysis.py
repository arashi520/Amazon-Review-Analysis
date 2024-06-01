import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@st.cache_data
def load_data(path):
    data = pd.read_json('data/output_data_item.jsonl', lines=True, orient='records')
    data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
    data['rating_number'] = pd.to_numeric(data['rating_number'], errors='coerce')
    data['main_category'] = data['main_category'].astype(str)
    data['store'] = data['store'].astype(str)
    return data.copy()

# read the data
data = load_data('https://raw.githubusercontent.com/arashi520/Amazon-Review-Analysis/main/data/output_data_item.jsonl')


# filter the top ten stores with the most rating_number 
data_cleaned = data[data['store'] != 'None']
top_stores = data_cleaned['store'].value_counts().head(10)

# Create a bar chart showing the number of ratings for the top ten stores
st.write("### Top 10 Stores by Rating Number")
st.bar_chart(top_stores)


# Filter products with rating_number greater than 50 and plot the distribution of average_rating
filtered_data = data[data['rating_number'] > 50]
fig = px.histogram(filtered_data, x='average_rating', title='Distribution of Average Rating for Products with Rating Number > 50')
st.write("### Distribution of Average Rating for Products with Rating Number > 50")
st.plotly_chart(fig)

# Filter the titles of the top 100 products with the most rating_number and generate word cloud
top_titles = data.sort_values('rating_number', ascending=False).head(100)['title']
wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(' '.join(top_titles))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.write("### Word Cloud of Top 100 Titles by Rating Number")
st.pyplot(plt)

import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@st.cache()
def load_data(path):
    data = pd.read_json("/Users/chenyarou/Desktop/output_data_item.json", lines=True)
    data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')
    data['rating_number'] = pd.to_numeric(data['rating_number'], errors='coerce')
    data['main_category'] = data['main_category'].astype(str)
    data['store'] = data['store'].astype(str)
    return data.copy()

# read the data
data = load_data('output_data_item.jsonl')

# 筛选 rating_number 最多的前十个 store
top_stores = data['store'].value_counts().head(10)

# 创建条形图显示前十个 store 的评分数量
st.write("### Top 10 Stores by Rating Number")
st.bar_chart(top_stores)

# 筛选 rating_number 大于 50 的产品，并绘制 average_rating 的分布图
filtered_data = data[data['rating_number'] > 50]
fig = px.histogram(filtered_data, x='average_rating', title='Distribution of Average Rating for Products with Rating Number > 50')
st.write("### Distribution of Average Rating for Products with Rating Number > 50")
st.plotly_chart(fig)

# 筛选 rating_number 最多的前 100 个产品的 title，并生成 word cloud
top_titles = data.sort_values('rating_number', ascending=False).head(100)['title']
wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(' '.join(top_titles))
st.write("### Word Cloud of Top 100 Titles by Rating Number")
st.image(wordcloud.to_array(), use_column_width=True)

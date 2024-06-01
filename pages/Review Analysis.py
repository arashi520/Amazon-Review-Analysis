import streamlit as st
import pandas as pd
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取JSONL文件
def load_data(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return pd.DataFrame(data)

# 加载数据
data_filepath = 'Amazon-Review-Analysis/data/All_Beauty.jsonl'
df = load_data(data_filepath)

# 设置 Streamlit 页面标题
st.title("Amazon Review Analysis")

# 显示评分分布
st.subheader("Review Ratings Distribution")
rating_counts = df['rating'].value_counts().sort_index()
st.bar_chart(rating_counts)

# 显示 helpful_vote 数量分布(turns out非常不均匀)
st.subheader("Helpful Vote Distribution")
plt.figure(figsize=(10, 5))
plt.hist(df['helpful_vote'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Helpful Votes')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Helpful Votes')
st.pyplot(plt)

# 显示最有帮助的前10条评论
st.subheader("Top 10 Reviews with Most Helpful Votes")
top_10_helpful_reviews = df.nlargest(10, 'helpful_vote')[['user_id', 'rating', 'text', 'helpful_vote']]
st.write(top_10_helpful_reviews)

# 显示评论内容的词云
st.subheader("Word Cloud of Review Text")
text = " ".join(review for review in df['text'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
st.pyplot(plt)

# 运行 Streamlit 应用
if __name__ == "__main__":
    st.run()

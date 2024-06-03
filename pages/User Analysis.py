import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def load_css(css_file):
    """Load the CSS file"""
    with open(css_file, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_data(path):
    with open(path, 'r') as file:
        data = [json.loads(line) for line in file]
    df = pd.DataFrame(data)
    if 'age' in df.columns and not df['age'].isnull().all():
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df['age'] = pd.cut(df['age'], bins=[0, 20, 30, 40, 50, 60, 70, np.inf], labels=[
        'Under 20', '20-30', '30-40', '40-50', '50-60', '60-70', 'Above 70'])
    return df
    
    
def plot_line_chart(data):  
    # Ensure the timestamp column is in datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    
    # Drop rows with invalid timestamps
    data = data.dropna(subset=['timestamp'])
      
    # Create a year-month column for grouping
    data['timestamp'] = data['timestamp'].dt.to_period('M')
    
    # Group by year-month and calculate the median sold price
    grouped_data = data.groupby('timestamp')['user_id'].count().reset_index()
    grouped_data['timestamp'] = grouped_data['timestamp'].dt.to_timestamp()

    # Plot the line chart
    fig = px.line(grouped_data, x='timestamp', y='user_id', title='Number of Reviewers Over Time')
    fig.update_layout(xaxis_title='Year-Month', yaxis_title='Number of Reviewed Users', template='plotly_white')

    return fig



def plot_horizontal_bar_chart(data, column, isTag=True):
    # Filter out null values
    data = data.dropna(subset=[column])

    # Group by the specified column and count occurrences
    grouped_data = data[column].value_counts().reset_index()
    grouped_data.columns = [column, 'count']

    # Plot the horizontal bar chart
    fig = px.bar(grouped_data, x='count', y=column, orientation='h', title=f'{column.capitalize()} by Total Count')
    fig.update_layout(xaxis_title='Total Count', yaxis_title=f'{column.capitalize()}', template='plotly_white')

    # Conditionally set the textposition based on the isTag parameter
    if isTag:
        fig.update_traces(textposition='outside', text=grouped_data['count'])
    else:
        fig.update_traces(textposition='none')

    # Explicitly set the category order for the y-axis to ensure descending order
    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    return fig


def plot_donut_chart(data, column):
    # Filter out null values
    data = data.dropna(subset=column)
    
    # Group by hasView and count occurrences
    grouped_data = data[column].value_counts().reset_index()
    grouped_data.columns = [column, 'count']

    # Plot the donut chart
    fig = go.Figure(data=[go.Pie(labels=grouped_data[column], values=grouped_data['count'], hole=.3)])
    fig.update_layout(title_text=f'Distribution of {column.capitalize()}')

    return fig

def main():
    st.title("Amazon User Analysis")

    # Load the CSS file
    load_css("asset/style.css")
    
    # Load data
    user_data = load_data("data/output_data_user.jsonl")
    review_data = load_data("data/output_data_review.jsonl")
    merged_data = pd.merge(review_data[['user_id']], user_data, on='user_id', how='left')

   # Header
    st.markdown("""
        <div class="header-container">
            <header class="header-text">IMT 563 Advanced Database Management System @ Amazon All Beauty Category Reviews 2023 Data Visualization</header>
        </div>
    """, unsafe_allow_html=True)

    #Plot charts
    line_chart = plot_line_chart(review_data)
    bar_chart = plot_horizontal_bar_chart(merged_data, 'age', isTag=True)
    donut_chart = plot_donut_chart(merged_data, 'gender')

    st.plotly_chart(line_chart, use_container_width=True)
    st.plotly_chart(donut_chart, use_container_width=True)
    st.plotly_chart(bar_chart, use_container_width=True)


  

    


if __name__ == "__main__":
    main()

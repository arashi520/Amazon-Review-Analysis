import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#######################################
# PAGE SETUP
#######################################
def load_css(css_file):
    """Load the CSS file"""
    with open(css_file, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_data(path):
    with open(path, 'r') as file:
        data = [json.loads(line) for line in file]
    df = pd.DataFrame(data)
    return df
    
    
def plot_line_chart(data, neighborhood, date_range):    
    # Create a year-month column for grouping
    data['year_month'] = data['dateSoldString'].dt.to_period('M')
    
    # Group by year-month and calculate the median sold price
    grouped_data = data.groupby('year_month')['price'].median().reset_index()
    grouped_data['year_month'] = grouped_data['year_month'].dt.to_timestamp()

    # Plot the line chart
    fig = px.line(grouped_data, x='year_month', y='price', title='Median Sold Price Over Time')
    fig.update_layout(xaxis_title='Year-Month', yaxis_title='Median Sold Price', template='plotly_white')

    return fig

def plot_vertical_bar_chart(data, column, isTag=True):
    # Filter out null values
    data = data.dropna(subset=[column])
    
    # Group by the specified column and count occurrences
    grouped_data = data[column].value_counts().reset_index()
    grouped_data.columns = [column, 'count']
    
    # Sort the data in descending order
    grouped_data = grouped_data.sort_values(by='count', ascending=False)
    
    # Plot the vertical bar chart
    fig = px.bar(grouped_data, x=column, y='count', title=f'Total Count of {column.capitalize()}', text='count')
    fig.update_layout(template='plotly_white')

    # Conditionally set the textposition based on the isTag parameter
    if isTag:
        fig.update_traces(textposition='outside')
    else:
        fig.update_traces(textposition='none')
    
    # Explicitly set the category order for the x-axis
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    
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


def plot_top10_horizontal_bar_chart(data, column, isTag=True):
    # Filter out null values
    data = data.dropna(subset=[column])

    # Group by the specified column and count occurrences
    grouped_data = data[column].value_counts().reset_index()
    grouped_data.columns = [column, 'count']

    # Sort by the total amount and select the top 10
    top_10 = grouped_data.nlargest(10, 'count')

    # Plot the horizontal bar chart
    fig = px.bar(top_10, x='count', y=column, orientation='h', title=f'Top {len(top_10)} {column.capitalize()} by Total Count')
    fig.update_layout(xaxis_title='Total Count', yaxis_title=f'{column.capitalize()}', template='plotly_white')

    # Conditionally set the textposition based on the isTag parameter
    if isTag:
        fig.update_traces(textposition='outside', text=top_10['count'])
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
    # Configure page settings
    st.set_page_config(
        page_title="Amazon All Beauty Dashboard",
        page_icon="🏠",
        layout="wide"
    )

    st.title("Amazon All Beauty Category Analysis: User Profile")

    # Load the CSS file
    load_css("asset/style.css")
    
    # Load data
    data = load_data("data/output_data_user.jsonl")

    # Header
    st.markdown("""
        <div class="header-container">
            <header class="header-text">Wayber@Seattle: proptotype dashboard for testing purpose</header>
        </div>
    """, unsafe_allow_html=True)

  

    # Sidebar
    # Sidebar filters
    # st.sidebar.markdown("# Filters")
    
    # neighborhoods = ["All"] + sorted(data['subdivisionName'].dropna().unique().tolist())
    # selected_neighborhood = st.sidebar.selectbox("Select Neighborhood", neighborhoods)

    # min_date = data['dateSoldString'].min().date()
    # max_date = data['dateSoldString'].max().date()
    # date_range = st.sidebar.slider("Select Date Range", min_date, max_date, (min_date, max_date))

    # # Filter the data based on the selected neighborhood and date range
    # if selected_neighborhood != "All":
    #     data = data[data['subdivisionName'] == selected_neighborhood]

    # start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    # data = data[(data['dateSoldString'] >= start_date) & (data['dateSoldString'] <= end_date)]

    # # Plot charts
    # line_chart = plot_line_chart(data, selected_neighborhood, date_range)
    # year_built_chart = plot_vertical_bar_chart(data, 'yearBuilt', False)
    # garage_spaces_chart = plot_vertical_bar_chart(data, 'garageSpaces')
    # zipcode_chart = plot_top10_horizontal_bar_chart(data, 'zipcode')
    # hasview_chart = plot_donut_chart(data, 'hasView')
    # hometype_chart = plot_donut_chart(data, 'homeType')
    # condition_chart = plot_horizontal_bar_chart(data, 'propertyCondition')
    # sewer_chart = plot_horizontal_bar_chart(data, 'sewer')
    # lot_spaces_chart = plot_vertical_bar_chart(data, 'lot_area_group')
    # living_spaces_chart = plot_vertical_bar_chart(data, 'living_area_group')
    # bedroom_chart = plot_vertical_bar_chart(data, 'bedrooms')
    # bathroom_chart = plot_vertical_bar_chart(data, 'bathrooms')
    # hoa_chart = plot_vertical_bar_chart(data, 'hoa_group')
    # ele_school_chart = plot_donut_chart(data, 'elementarySchool')
    # mid_school_chart = plot_donut_chart(data, 'middleSchool')
    # high_school_chart = plot_donut_chart(data, 'highSchool')
    

    # # Display charts in Streamlit
    # st.plotly_chart(line_chart, use_container_width=True)
    # st.plotly_chart(living_spaces_chart, use_container_width=True)
    # st.plotly_chart(year_built_chart, use_container_width=True)
    # st.plotly_chart(hometype_chart, use_container_width=True)
    # st.plotly_chart(bedroom_chart, use_container_width=True)
    # st.plotly_chart(condition_chart, use_container_width=True)
    # st.plotly_chart(hoa_chart, use_container_width=True)
    # st.plotly_chart(mid_school_chart, use_container_width=True)

        
    # with col2:
    #     st.plotly_chart(zipcode_chart, use_container_width=True)
    #     st.plotly_chart(lot_spaces_chart, use_container_width=True)
    #     st.plotly_chart(garage_spaces_chart, use_container_width=True)
    #     st.plotly_chart(hasview_chart, use_container_width=True)
    #     st.plotly_chart(bathroom_chart, use_container_width=True)
    #     st.plotly_chart(sewer_chart, use_container_width=True)
    #     st.plotly_chart(ele_school_chart, use_container_width=True)
    #     st.plotly_chart(high_school_chart, use_container_width=True)

    


        


if __name__ == "__main__":
    main()

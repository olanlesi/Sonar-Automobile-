import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from random import choice
import seaborn as sns


def run():
    st.title('Soran Automobile Presentation')
    st.sidebar.markdown("[Madey by Lacey](https://www.linkedin.com/in/olanlesi-banjo)", unsafe_allow_html=True)

run()

st.set_option('deprecation.showPyplotGlobalUse', False)
st.write("""
--------
This dashboard provides analysis on top 5 cars and model to determine customers' prefrence and help Sonar Automobile make inform decision 
""")

st.write("---")


def load_data():
    data = pd.read_csv("cleaned_soran_automobiles")
    return data

# Loading data
df = load_data()

df['year'] = pd.to_datetime(df['year'], format='%Y', errors='coerce').dt.year

# getting top 5 popular cars
top_5_cars = df['car'].value_counts().nlargest(5)
car_df = df[df['car'].isin(top_5_cars.index)]

# getting top 5 popular models
top_5_model = df['model'].value_counts().nlargest(5)
model_df = df[df['model'].isin(top_5_model.index)]

main_data = {'All Data':df, 'Car Data':car_df, 'Model Data':model_df}
# creating  sidebar element
st.sidebar.title('Select the features you will like to explore')
sel_data = st.sidebar.selectbox(
    'Explore base on which data:', list(main_data.keys())
)
if sel_data == []:
    sel_data =['All Data']
data=main_data[sel_data]

if sel_data == 'All Data':
    cat_col = ['body', 'engType', 'registration', 'drive']
else:
    cat_col = ['car', 'model', 'body', 'engType', 'registration', 'drive']
num_col = ['price', 'mileage', 'engV', 'year', 'count']

color = ['skyblue', 'pink', 'yellow', 'red', 'purple', 'blue', 'green']

st.subheader('Basic Infomation: ')
st.write(f"There are {data.shape[0]} rows and {data.shape[1]} features in the data")
st.write(f"The features includes {list(data.columns)}")

st.subheader('Basic Statistics: ')
st.write(data.describe().T)


chart_list = ['Boxplot', 'Barchart',  'Scatterplot', 'Piechart', 'Histogram', 'Linechart', 'Pairplot']

st.sidebar.subheader('Visualization')
select_chart = st.sidebar.selectbox(
    'Choose a Chart to Explore more:', chart_list
)

# pairplot
if select_chart == 'Pairplot':
    hue = st.sidebar.selectbox(
        'Select hue', cat_col
    )
    plt.figure(figsize=(30,15))
    sns.pairplot(data, hue=hue)
    st.write('Scratterplot of all numerical features')
    st.pyplot()

# barchart
if select_chart == 'Barchart':

    x = st.sidebar.selectbox(
        'Select x value', cat_col
    )
    y = st.sidebar.selectbox(
        'Select y value', num_col
    )
    hue = hue = st.sidebar.selectbox(
        'Select hue', cat_col
    )

    st.subheader(f'Barchart of {x} against {y}')
    if y == 'count':
        count_x = data[x].value_counts()
        st.bar_chart(count_x)
    else:
        plt.figure(figsize=(10,6))
        fig = px.bar(data, x=x, y=y, color=hue)
        st.plotly_chart(fig)


# Boxplot
if select_chart == 'Boxplot':
    x = st.sidebar.selectbox(
        'Select x value', num_col
    )
    y = st.sidebar.selectbox(
        'Select y value', cat_col
    )
    st.subheader(f'Boxplot of {x} against {y}')
    if x == 'count':
        st.write('Please chose another variable for x')
    else:
        plt.figure(figsize=(12, 20))
        sns.boxplot(data, y=y, x=x)
        st.pyplot()

# Piechart
if select_chart == 'Piechart':
    x = st.sidebar.selectbox(
        'Select x value', cat_col
    )
    st.subheader(f'Piechart of {x}')
    pie_data = data[x].value_counts().reset_index()
    pie_data.columns = ['values', 'count']

    fig = px.pie(pie_data, values='count', names='values')
    st.plotly_chart(fig)


# Scatterplot
if select_chart == 'Scatterplot':
    x = st.sidebar.selectbox(
        'Select x value', num_col
    )
    y = st.sidebar.selectbox(
        'Select y value', num_col
    )
    color = choice(cat_col)
    symbol = choice(cat_col)
    st.subheader(f'Scatterplot of {x} against {y}')
    if x == 'count' or y == 'count':
        st.write("Please don't chose 'count' for x or y variable")
    else:
        st.subheader(f'Showing Scatterplot of {x} against {y}')
        st.write(f'Differentiating each {color} by color and {symbol} by symbol')
        fig = px.scatter(data, x=x, y=y, color=color ,symbol=symbol )
        st.plotly_chart(fig)

# Linechart
if select_chart == 'Linechart':
    x = st.sidebar.selectbox(
        'Select x value', num_col
    )
    avg_type = st.sidebar.radio(
        'Chose meassure',['Mean', 'Median']
    )
    st.subheader(f'{avg_type} car {x} over the years')
    if x == 'count' or x == 'year':
        st.write("Please don't chose 'count' or 'year' for x variable")
    else:
        if avg_type == 'Median':
            avg = data.groupby('year')[x].median()
        else:
            avg = data.groupby('year')[x].mean()
        st.line_chart(avg)


# Histogram
if select_chart == 'Histogram':
    x = st.sidebar.selectbox(
        'Select x value', num_col
    )
    kde = st.sidebar.radio(
        'Choose True or False for kde', [True, False]
    )
    st.subheader(f'Distribution of {x}')
    if x == 'count':
        st.write("Please don't chose 'count' for x variable")
    else:
        plt.figure(figsize=(10, 6))
        sns.histplot(data[x], bins=30, kde=bool(kde))
        st.pyplot()

# streamlit run Dashboard.py

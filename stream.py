'''
Stock pridictor streamlit
to execute
open terminal in pycharm run below
streamlit run stream.py
https://www.youtube.com/watch?v=0E_31WqVzCY
'''

import streamlit as st
from datetime import date, timezone
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objects as go
import pandas as pd
import numpy as np


def option1():
    st.write("Yahoo Finance Futures")
    # Add your option 1 code here
    yahoo_finance()


def option2():
    st.write("Your Own Dataset")
    # Add your option 2 code here
    my_dataset()

def my_dataset():
    # Create a file uploader widget
    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file)
        return df

    st.title("File Uploader Example")
    st.write('Upload your own dataset in a CSV file')
    st.write(' format. The dataset should have two columns: Date and Price (spelled exact).')
    uploaded_file = st.file_uploader("Choose a file", type="csv")

    if uploaded_file is not None:
        df = load_data(uploaded_file)
            # Display file details
        st.write("File name:", uploaded_file.name)
        st.write("File type:", uploaded_file.type)
        st.write("File size:", uploaded_file.size, "bytes")
        st.write(df)
    
        n_years = st.slider('Years of prediction', 1, 4)
        period = n_years * 365
        data_load_state = st.text('Loading data...')
        data = df
        data_load_state.text('Loading data...done!')

        st.subheader('Raw data')
        st.write(data.tail())
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Price'], name='Your_Data_Price'))
            fig.layout.update(title_text=f'Your Price Series Data', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)

        plot_raw_data()

        # Forcasting using Prophet
        df_train = data[['Date','Price']]
        df_train = df_train.rename(columns={'Date': 'ds', 'Price': 'y'})

        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        st.write('Forecasted data')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write('Forcast components')
        fig2 = m.plot_components(forecast)
        st.write(fig2)

        st.subheader('Forecast data')
        st.write(forecast.tail())
    else:
        st.write("Unsupported file type, please upload a CSV file.")
def yahoo_finance():
    START = '1980-01-01'
    TODAY = date.today().strftime('%Y-%m-%d')

    st.title('Futures Price Prediction')
    st.markdown(':blue[**Phil Steichen**]')

    stocks = ('ZC=F', 'ZW=F', 'ZS=F','SPX')
    # stocks = ('AAPL','GOOG')
    selected_stock = st.selectbox('Select dataset for prediction',  stocks)

    n_years = st.slider('Years of prediction', 1, 4)
    period = n_years * 365

    @st.cache_data
    def load_data(stock):
        data = yf.download(stock, start=START, end=TODAY)
        data.reset_index(inplace=True)
        # data.replace(tzinfo=None)
        return data
    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data...done!')

    st.subheader('Raw data')
    st.write(data.tail())
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title_text=f'{selected_stock} Stock Price Series Data', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    # Forcasting using Prophet
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={'Date': 'ds', 'Close': 'y'})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.write('Forecasted data')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write('Forcast components')
    fig2 = m.plot_components(forecast)
    st.write(fig2)

    st.subheader('Forecast data')
    st.write(forecast.tail())
def page1():
    st.title("Price Predictor")
    st.title("Welcome to Phil's easy to use price analysis tool")
    st.write('This tool will help you to predict the future price of your favorite stock or commodity')
    st.write('You can choose to use Yahoo Finance Futures or upload your own dataset!')
    st.write('by Phil Steichen')

    # Initialize session state
    if 'option' not in st.session_state:
        st.session_state.option = None

    # Create buttons and update session state
    if st.button('Yahoo Finance Futures'):
        st.session_state.option = 'option1'

    if st.button('Your Own Dataset'):
        st.session_state.option = 'option2'

    # Run the function based on session state
    if st.session_state.option == 'option1':
        option1()
    elif st.session_state.option == 'option2':
        option2()

def hedgeAI():
    st.write("Comparing hedge estimates for different locations")
def page2():
    st.title("HedgeAI")
    st.write("This is the page for the thesis for the completion of MAB for Phil Steichen!")
    hedgeAI()

    
def main():
    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("HedgeAI","Price Predictor"))

    # Show the selected page
    if page == "Price Predictor":
        page1()
    elif page == "HedgeAI":
        page2()
if __name__ == '__main__':
    main()
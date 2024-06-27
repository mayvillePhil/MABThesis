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

def main():
    st.title("Non Yahoo Finance Data Uploader")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Choose a file", type="csv")

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Display file details
        st.write("File name:", uploaded_file.name)
        st.write("File type:", uploaded_file.type)
        st.write("File size:", uploaded_file.size, "bytes")
        df = pd.read_csv(uploaded_file)
        st.write(df)
    else:
        st.write("Unsupported file type, please upload a CSV file.")

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

if __name__ == '__main__':
    main()
import streamlit as st
import pandas as pd
import numpy as np
import requests
import config 
import psycopg2, psycopg2.extras
import plotly.graph_objects as go
import yfinance as yf
from datetime import date
import main

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


option = st.sidebar.selectbox("Which Dashboard?", ('Chart', 'Stocktwits','Predictions'))

st.header(option)



if option == 'Chart':
    symbol = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')

    ticker1 = yf.Ticker(symbol)
    data = ticker1.history(symbol,start = START, end = TODAY,interval = '1d')
    st.subheader(symbol.upper())

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name=symbol)])

    fig.update_xaxes(type='category')
    fig.update_layout(height=700)

    st.plotly_chart(fig, use_container_width=True)

    st.write(data)




if option == 'Stocktwits':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])


if option == 'Predictions':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=5)
    st.title('Stock Forecast App')
    n_years = st.slider('Years of data to consider for prediction:', 1, 4)
    main.make_stock_prediction(symbol, n_years)


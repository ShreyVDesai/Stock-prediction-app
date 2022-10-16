# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
from pmdarima.arima import auto_arima
import yfinance as yf
import plotly.express as px
from plotly import graph_objs as go
import numpy as np
import pandas as pd
import datetime

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

def make_stock_prediction(tick,n_years):
	

	period = n_years * 365


	

	
	data_load_state = st.text('Loading data...')
	global data
	data = load_data(tick)
	data_load_state.text('Loading data... done!')

	st.subheader('Raw data')
	st.write(data.tail())

	plot_raw_data()

	# Predict forecast with autoariima.
	df_train = data[['Date','Close']]
	df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

	pred_load_state = st.text("Please wait while we load your data")

	auto_model = auto_arima(df_train['y'], m=4, seasonal=True,suppress_warnings = True,  step_wise=True, trace=True)
	global forecast
	forecast = pd.DataFrame(auto_model.predict(n_periods = period),index = pd.date_range(start = df_train['ds'].iloc[-1]+datetime.timedelta(days=1),periods = period))

	pred_load_state.text('Your prediction is now ready!')
	return forecast



# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	




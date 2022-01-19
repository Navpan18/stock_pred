# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock | Crypto Price Forecaster')
selected_stock = st.text_input('Enter ticker',key="lkj345gt56frtd")

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data
def com_check(ticker):
    msft = yf.Ticker(ticker)
    return msft.info

if(selected_stock==''):
    selected_stock='GOOG'

	
data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
com_name = com_check(selected_stock)
data_load_state.text('Loading data... done!')


if(com_name['quoteType']=='CRYPTOCURRENCY'):
    st.header(com_name['name'])
    with st.expander("See crypto summary"):
        st.write(com_name['description'])
else:
    st.header((com_name['longName']))
    with st.expander("See business summary"):
        st.image(com_name['logo_url'])
        st.write(com_name['longBusinessSummary'])


st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

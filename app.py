# app.py
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os

# ======================
# 1. 读取 CSV
# ======================
data_path = "data/stock_data_sample.csv"

if not os.path.exists(data_path):
    st.error(f"CSV file not found at {data_path}. Please make sure 'stock_data_sample.csv' is in the data/ folder.")
    st.stop()

# 读取数据并解析日期
data = pd.read_csv(data_path, parse_dates=['DlyCalDt'])

# 重命名列便于分析
data.rename(columns={
    'DlyCalDt': 'Date',
    'DlyPrc': 'Close',
    'DlyOpen': 'Open',
    'DlyHigh': 'High',
    'DlyLow': 'Low',
    'DlyVol': 'Volume'
}, inplace=True)

# 按股票+日期排序
data = data.sort_values(by=['Ticker', 'Date'])

# ======================
# 2. 计算指标
# ======================
# 每日收益率
data['Daily_Return'] = data.groupby('Ticker')['Close'].pct_change()

# 移动均线
data['MA_7'] = data.groupby('Ticker')['Close'].transform(lambda x: x.rolling(7).mean())
data['MA_30'] = data.groupby('Ticker')['Close'].transform(lambda x: x.rolling(30).mean())

# 30 日滚动波动率
data['Volatility_30'] = data.groupby('Ticker')['Daily_Return'].transform(lambda x: x.rolling(30).std())

# ======================
# 3. Streamlit 界面
# ======================
st.set_page_config(page_title="Interactive Stock Analysis", layout="wide")
st.title("Interactive Stock Analysis Tool")

# 选择股票
tickers = data['Ticker'].unique().tolist()
selected_tickers = st.multiselect("Select one or more stocks:", tickers, default=tickers)

# 选择时间范围
min_date = data['Date'].min()
max_date = data['Date'].max()
start_date, end_date = st.date_input(
    "Select date range:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# 过滤数据
filtered_data = data[
    (data['Ticker'].isin(selected_tickers)) &
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]

if filtered_data.empty:
    st.warning("No data available for the selected stocks and date range.")
    st.stop()

# ======================
# 4. 绘图：收盘价 + 移动均线
# ======================
st.subheader("Stock Price with Moving Averages")
fig_price = go.Figure()
for ticker in selected_tickers:
    df = filtered_data[filtered_data['Ticker'] == ticker]
    fig_price.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name=f"{ticker} Close"))
    fig_price.add_trace(go.Scatter(x=df['Date'], y=df['MA_7'], mode='lines', name=f"{ticker} MA7", line=dict(dash='dot')))
    fig_price.add_trace(go.Scatter(x=df['Date'], y=df['MA_30'], mode='lines', name=f"{ticker} MA30", line=dict(dash='dash')))

fig_price.update_layout(height=500, width=1000, xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig_price, use_container_width=True)

# ======================
# 5. 日收益率直方图
# ======================
st.subheader("Daily Return Distribution")
for ticker in selected_tickers:
    df = filtered_data[filtered_data['Ticker'] == ticker]
    fig_hist = px.histogram(df, x='Daily_Return', nbins=50, title=f"{ticker} Daily Return Histogram")
    st.plotly_chart(fig_hist, use_container_width=True)

# ======================
# 6. 30 日滚动波动率
# ======================
st.subheader("30-Day Rolling Volatility")
fig_vol = go.Figure()
for ticker in selected_tickers:
    df = filtered_data[filtered_data['Ticker'] == ticker]
    fig_vol.add_trace(go.Scatter(x=df['Date'], y=df['Volatility_30'], mode='lines', name=f"{ticker} Volatility"))

fig_vol.update_layout(height=500, width=1000, xaxis_title='Date', yaxis_title='Volatility')
st.plotly_chart(fig_vol, use_container_width=True)

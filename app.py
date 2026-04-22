import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/stock_data.csv")
    df['DlyCalDt'] = pd.to_datetime(df['DlyCalDt'])
    df = df[df['Ticker'].isin(['AAPL','MSFT','AMZN','TSLA'])]
    df.sort_values(['Ticker','DlyCalDt'], inplace=True)
    return df

data = load_data()

# ----------------------------
# Sidebar - User Inputs
# ----------------------------
st.sidebar.header("Stock Selection & Date Range")
selected_stocks = st.sidebar.multiselect(
    "Select Stocks", options=['AAPL','MSFT','AMZN','TSLA'], default=['AAPL','MSFT','AMZN','TSLA']
)

start_date = st.sidebar.date_input("Start Date", datetime(2020,1,1))
end_date = st.sidebar.date_input("End Date", datetime(2025,12,31))

show_ma = st.sidebar.checkbox("Show 50-Day Moving Average", value=True)
show_corr = st.sidebar.checkbox("Show Correlation Heatmap", value=True)
show_portfolio = st.sidebar.checkbox("Show Equal-Weight Portfolio", value=True)

# Filter data
df_filtered = data[(data['Ticker'].isin(selected_stocks)) &
                   (data['DlyCalDt'] >= pd.to_datetime(start_date)) &
                   (data['DlyCalDt'] <= pd.to_datetime(end_date))]

# ----------------------------
# Main App
# ----------------------------
st.title("Interactive Stock Analysis Tool")
st.write("Visualize and analyze historical stock data for selected tech companies.")

# ----------------------------
# Adjusted Close Price Plot
# ----------------------------
st.subheader("Adjusted Close Price")
plt.figure(figsize=(10,5))
for ticker in selected_stocks:
    df_t = df_filtered[df_filtered['Ticker']==ticker].copy()
    df_t['AdjClose'] = df_t['DlyPrc']  # Assuming DlyPrc as adjusted close
    if show_ma:
        df_t['MA50'] = df_t['AdjClose'].rolling(window=50).mean()
        plt.plot(df_t['DlyCalDt'], df_t['MA50'], linestyle='--', label=f"{ticker} 50-Day MA")
    plt.plot(df_t['DlyCalDt'], df_t['AdjClose'], label=ticker)
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
st.pyplot(plt.gcf())
plt.clf()

# ----------------------------
# Daily Returns Plot
# ----------------------------
st.subheader("Daily Returns")
plt.figure(figsize=(10,5))
for ticker in selected_stocks:
    df_t = df_filtered[df_filtered['Ticker']==ticker].copy()
    df_t['DailyReturn'] = df_t['AdjClose'].pct_change()
    plt.plot(df_t['DlyCalDt'], df_t['DailyReturn'], label=ticker)
plt.xlabel("Date")
plt.ylabel("Daily Return")
plt.legend()
st.pyplot(plt.gcf())
plt.clf()

# ----------------------------
# Correlation Heatmap
# ----------------------------
if show_corr and len(selected_stocks)>1:
    st.subheader("Correlation Heatmap")
    pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='DlyPrc')
    corr = pivot_df[selected_stocks].corr()
    plt.figure(figsize=(6,5))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    st.pyplot(plt.gcf())
    plt.clf()

# ----------------------------
# Equal-weight Portfolio
# ----------------------------
if show_portfolio and len(selected_stocks)>1:
    st.subheader("Equal-Weight Portfolio Cumulative Return")
    pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='DlyPrc')
    daily_returns = pivot_df[selected_stocks].pct_change().fillna(0)
    portfolio_return = daily_returns.mean(axis=1)
    cumulative_return = (1 + portfolio_return).cumprod()
    plt.figure(figsize=(10,5))
    plt.plot(cumulative_return.index, cumulative_return.values, label='Portfolio')
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

# ----------------------------
# Download Filtered Data
# ----------------------------
st.subheader("Download Filtered Data")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_stock_data.csv',
    mime='text/csv',
)

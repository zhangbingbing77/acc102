import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ----------------------------
# Streamlit style
# ----------------------------
st.set_page_config(layout="wide")
sns.set_style("whitegrid")

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

# ----------------------------
# Filter data
# ----------------------------
@st.cache_data
def filter_data(data, stocks, start, end):
    df = data[(data['Ticker'].isin(stocks)) &
              (data['DlyCalDt'] >= pd.to_datetime(start)) &
              (data['DlyCalDt'] <= pd.to_datetime(end))].copy()
    df['AdjClose'] = df['DlyPrc']
    df['DailyReturn'] = df.groupby('Ticker')['AdjClose'].pct_change()
    return df

df_filtered = filter_data(data, selected_stocks, start_date, end_date)

# ----------------------------
# Main App
# ----------------------------
st.title("Interactive Stock Analysis Tool")
st.write("Visualize and analyze historical stock data for selected tech companies.")

# ----------------------------
# Adjusted Close Price Plot
# ----------------------------
st.subheader("Adjusted Close Price")
fig, ax = plt.subplots(figsize=(12,6))
palette = sns.color_palette("tab10", n_colors=len(selected_stocks))

for i, ticker in enumerate(selected_stocks):
    df_t = df_filtered[df_filtered['Ticker']==ticker]
    ax.plot(df_t['DlyCalDt'], df_t['AdjClose'], label=ticker, color=palette[i])
    if show_ma:
        df_t['MA50'] = df_t['AdjClose'].rolling(window=50).mean()
        ax.plot(df_t['DlyCalDt'], df_t['MA50'], linestyle='--', color=palette[i], alpha=0.7)

ax.set_xlabel("Date")
ax.set_ylabel("Price ($)")
ax.legend()
st.pyplot(fig)

# ----------------------------
# Daily Returns Plot
# ----------------------------
st.subheader("Daily Returns")
fig, ax = plt.subplots(figsize=(12,6))
for i, ticker in enumerate(selected_stocks):
    df_t = df_filtered[df_filtered['Ticker']==ticker]
    ax.plot(df_t['DlyCalDt'], df_t['DailyReturn'], label=ticker, color=palette[i])
ax.set_xlabel("Date")
ax.set_ylabel("Daily Return")
ax.legend()
st.pyplot(fig)

# ----------------------------
# Correlation Heatmap
# ----------------------------
if show_corr and len(selected_stocks) > 1:
    st.subheader("Correlation Heatmap")
    pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
    corr = pivot_df[selected_stocks].corr()
    fig, ax = plt.subplots(figsize=(6,5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# ----------------------------
# Equal-weight Portfolio
# ----------------------------
if show_portfolio and len(selected_stocks) > 1:
    st.subheader("Equal-Weight Portfolio Cumulative Return")
    pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
    daily_returns = pivot_df[selected_stocks].pct_change().fillna(0)
    portfolio_return = daily_returns.mean(axis=1)
    cumulative_return = (1 + portfolio_return).cumprod()

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(cumulative_return.index, cumulative_return.values, label='Portfolio', color='black', linewidth=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.legend()
    st.pyplot(fig)

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

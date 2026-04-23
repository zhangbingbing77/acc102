import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ----------------------------
# Streamlit page configuration
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
# Sidebar inputs
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
# Filter and preprocess data
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
# Investment advice function
# ----------------------------
def generate_investment_advice(df, stocks):
    advice = []

    # Cumulative return analysis
    cumulative_returns = df.groupby('Ticker')['AdjClose'].apply(lambda x: x.iloc[-1]/x.iloc[0]-1)
    top_stock = cumulative_returns.idxmax()
    bottom_stock = cumulative_returns.idxmin()
    advice.append(f"Highest cumulative return: {top_stock} ({cumulative_returns[top_stock]:.2%})")
    advice.append(f"Lowest cumulative return: {bottom_stock} ({cumulative_returns[bottom_stock]:.2%})")

    # Volatility analysis
    volatility = df.groupby('Ticker')['DailyReturn'].std()
    high_vol = volatility.idxmax()
    low_vol = volatility.idxmin()
    advice.append(f"Highest volatility stock: {high_vol} ({volatility[high_vol]:.2%})")
    advice.append(f"Lowest volatility stock: {low_vol} ({volatility[low_vol]:.2%})")

    # Trend analysis (price vs MA50)
    if show_ma:
        trend_advice = []
        for ticker in stocks:
            df_t = df[df['Ticker']==ticker].copy()
            df_t['MA50'] = df_t['AdjClose'].rolling(window=50).mean()
            if df_t['AdjClose'].iloc[-1] > df_t['MA50'].iloc[-1]:
                trend_advice.append(f"{ticker}: bullish trend ↑")
            else:
                trend_advice.append(f"{ticker}: pullback risk ↓")
        advice.append("Trend analysis: " + "; ".join(trend_advice))

    # Portfolio correlation analysis
    if len(stocks) > 1:
        pivot_df = df.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
        corr = pivot_df[stocks].pct_change().corr()
        high_corr_pairs = [(i,j,corr.loc[i,j]) for i in stocks for j in stocks if i<j and corr.loc[i,j]>0.8]
        if high_corr_pairs:
            pairs_str = ", ".join([f"{i}-{j} ({c:.2f})" for i,j,c in high_corr_pairs])
            advice.append(f"High correlation stock pairs: {pairs_str} (low diversification)")
        else:
            advice.append("Stock correlation moderate, portfolio well diversified")

    return advice

# ----------------------------
# Main app
# ----------------------------
st.title("Interactive Stock Analysis Tool")
st.write("Visualize and analyze historical stock data for selected tech companies.")

# ----------------------------
# Layout: 2 columns (charts | investment advice)
# ----------------------------
col1, col2 = st.columns([3,1])

# ----------------------------
# Charts column
# ----------------------------
with col1:
    # Adjusted Close Price + MA50
    st.subheader("Adjusted Close Price")
    fig, ax = plt.subplots(figsize=(12,5))
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

    # Daily Returns
    st.subheader("Daily Returns")
    fig, ax = plt.subplots(figsize=(12,5))
    for i, ticker in enumerate(selected_stocks):
        df_t = df_filtered[df_filtered['Ticker']==ticker]
        ax.plot(df_t['DlyCalDt'], df_t['DailyReturn'], label=ticker, color=palette[i])
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Return")
    ax.legend()
    st.pyplot(fig)

    # Correlation Heatmap
    if show_corr and len(selected_stocks) > 1:
        st.subheader("Correlation Heatmap")
        pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
        corr = pivot_df[selected_stocks].pct_change().corr()
        fig, ax = plt.subplots(figsize=(6,5))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Equal-weight Portfolio
    if show_portfolio and len(selected_stocks) > 1:
        st.subheader("Equal-Weight Portfolio Cumulative Return")
        pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
        daily_returns = pivot_df[selected_stocks].pct_change().fillna(0)
        portfolio_return = daily_returns.mean(axis=1)
        cumulative_return = (1 + portfolio_return).cumprod()
        fig, ax = plt.subplots(figsize=(12,5))
        ax.plot(cumulative_return.index, cumulative_return.values, label='Portfolio', color='black', linewidth=2)
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Return")
        ax.legend()
        st.pyplot(fig)

# ----------------------------
# Investment advice column
# ----------------------------
with col2:
    st.subheader("💡 Investment Advice")
    advice = generate_investment_advice(df_filtered, selected_stocks)
    for item in advice:
        st.write(item)

# ----------------------------
# Download filtered data
# ----------------------------
st.subheader("Download Filtered Data")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_stock_data.csv',
    mime='text/csv',
)

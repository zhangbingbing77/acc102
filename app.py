import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")

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

    cumulative_returns = df.groupby('Ticker')['AdjClose'].apply(lambda x: x.iloc[-1]/x.iloc[0]-1)
    top_stock = cumulative_returns.idxmax()
    bottom_stock = cumulative_returns.idxmin()
    advice.append(f"Highest cumulative return: {top_stock} ({cumulative_returns[top_stock]:.2%})")
    advice.append(f"Lowest cumulative return: {bottom_stock} ({cumulative_returns[bottom_stock]:.2%})")

    volatility = df.groupby('Ticker')['DailyReturn'].std()
    high_vol = volatility.idxmax()
    low_vol = volatility.idxmin()
    advice.append(f"Highest volatility stock: {high_vol} ({volatility[high_vol]:.2%})")
    advice.append(f"Lowest volatility stock: {low_vol} ({volatility[low_vol]:.2%})")

    if show_ma:
        trend_advice = []
        for ticker in stocks:
            df_t = df[df['Ticker']==ticker].copy()
            df_t['MA50'] = df_t['AdjClose'].rolling(50).mean()
            if df_t['AdjClose'].iloc[-1] > df_t['MA50'].iloc[-1]:
                trend_advice.append(f"{ticker}: bullish trend ↑")
            else:
                trend_advice.append(f"{ticker}: pullback risk ↓")
        advice.append("Trend analysis: " + "; ".join(trend_advice))

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

col1, col2 = st.columns([3,1])

# ----------------------------
# Charts column
# ----------------------------
with col1:
    # Adjusted Close + MA50
    st.subheader("Adjusted Close Price")
    fig = go.Figure()
    for ticker in selected_stocks:
        df_t = df_filtered[df_filtered['Ticker']==ticker]
        fig.add_trace(go.Scatter(x=df_t['DlyCalDt'], y=df_t['AdjClose'], mode='lines', name=ticker))
        if show_ma:
            df_t['MA50'] = df_t['AdjClose'].rolling(50).mean()
            fig.add_trace(go.Scatter(x=df_t['DlyCalDt'], y=df_t['MA50'], mode='lines', 
                                     name=f"{ticker} MA50", line=dict(dash='dash')))
    fig.update_layout(xaxis_title='Date', yaxis_title='Price ($)')
    st.plotly_chart(fig, use_container_width=True)

    # Daily Returns
    st.subheader("Daily Returns")
    fig = go.Figure()
    for ticker in selected_stocks:
        df_t = df_filtered[df_filtered['Ticker']==ticker]
        fig.add_trace(go.Scatter(x=df_t['DlyCalDt'], y=df_t['DailyReturn'], mode='lines', name=ticker))
    fig.update_layout(xaxis_title='Date', yaxis_title='Daily Return')
    st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    if show_corr and len(selected_stocks) > 1:
        st.subheader("Correlation Heatmap")
        pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
        corr = pivot_df[selected_stocks].pct_change().corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

    # Equal-weight Portfolio
    if show_portfolio and len(selected_stocks) > 1:
        st.subheader("Equal-Weight Portfolio Cumulative Return")
        pivot_df = df_filtered.pivot(index='DlyCalDt', columns='Ticker', values='AdjClose')
        daily_returns = pivot_df[selected_stocks].pct_change().fillna(0)
        portfolio_return = daily_returns.mean(axis=1)
        cumulative_return = (1 + portfolio_return).cumprod()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cumulative_return.index, y=cumulative_return.values, 
                                 mode='lines', name='Portfolio', line=dict(color='black', width=2)))
        fig.update_layout(xaxis_title='Date', yaxis_title='Cumulative Return')
        st.plotly_chart(fig, use_container_width=True)

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

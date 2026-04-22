# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ------------------------------
# 1. 页面标题
# ------------------------------
st.set_page_config(page_title="Interactive Stock Analysis Tool", layout="wide")
st.title("Interactive Stock Analysis Tool (AAPL, MSFT, AMZN, TSLA)")

# ------------------------------
# 2. 读取数据
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/stocks.csv")  # 相对路径
    df['date'] = pd.to_datetime(df['date'])
    df['Adj Close'] = df['prc'].abs()   # 确保收盘价正值
    df.sort_values(['ticker', 'date'], inplace=True)
    # 计算日收益率
    df['Daily Return'] = df.groupby('ticker')['Adj Close'].pct_change()
    return df

df = load_data()

# ------------------------------
# 3. 侧边栏交互选项
# ------------------------------
tickers = df['ticker'].unique()
selected_tickers = st.sidebar.multiselect("Select Stocks", tickers, default=tickers)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-12-31"))

show_moving_avg = st.sidebar.checkbox("Show 50-Day Moving Average", value=True)
show_corr = st.sidebar.checkbox("Show Daily Return Correlation Heatmap", value=True)
show_portfolio = st.sidebar.checkbox("Show Equal-Weight Portfolio", value=True)

# 筛选数据
data_filtered = df[
    (df['ticker'].isin(selected_tickers)) &
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
]

# ------------------------------
# 4. 收盘价趋势
# ------------------------------
st.subheader("Adjusted Close Price Trend")
fig, ax = plt.subplots(figsize=(10,5))
for ticker in selected_tickers:
    temp = data_filtered[data_filtered['ticker']==ticker]
    ax.plot(temp['date'], temp['Adj Close'], label=ticker)
    if show_moving_avg:
        ax.plot(temp['date'], temp['Adj Close'].rolling(50).mean(), linestyle='--', label=f"{ticker} 50-day MA")
ax.set_xlabel("Date")
ax.set_ylabel("Price ($)")
ax.legend()
st.pyplot(fig)

# ------------------------------
# 5. 日收益率折线图
# ------------------------------
st.subheader("Daily Return")
fig2, ax2 = plt.subplots(figsize=(10,5))
for ticker in selected_tickers:
    temp = data_filtered[data_filtered['ticker']==ticker]
    ax2.plot(temp['date'], temp['Daily Return'], label=ticker)
ax2.set_xlabel("Date")
ax2.set_ylabel("Daily Return")
ax2.legend()
st.pyplot(fig2)

# ------------------------------
# 6. 日收益率相关性
# ------------------------------
if show_corr and len(selected_tickers) > 1:
    st.subheader("Daily Return Correlation Heatmap")
    pivot = data_filtered.pivot(index='date', columns='ticker', values='Daily Return')
    corr = pivot[selected_tickers].corr()
    fig3, ax3 = plt.subplots(figsize=(6,5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

# ------------------------------
# 7. 简单等权组合累积收益率
# ------------------------------
if show_portfolio and len(selected_tickers) > 1:
    st.subheader("Equal-Weight Portfolio Cumulative Return")
    pivot = data_filtered.pivot(index='date', columns='ticker', values='Daily Return')
    portfolio_ret = pivot[selected_tickers].mean(axis=1)
    cumulative = (1 + portfolio_ret).cumprod()
    fig4, ax4 = plt.subplots(figsize=(10,5))
    ax4.plot(cumulative.index, cumulative, label="Portfolio")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Cumulative Return")
    st.pyplot(fig4)

# ------------------------------
# 8. 数据下载
# ------------------------------
st.subheader("Download Filtered Data")
st.write(data_filtered)
csv = data_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_stocks.csv',
    mime='text/csv',
)

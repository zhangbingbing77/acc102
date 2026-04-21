import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------
# Page config
# ----------------------
st.set_page_config(page_title="Tech Stock Decision Assistant", layout="wide")

st.title("📊 Tech Stock Decision Assistant")
st.markdown("ساعد retail investors compare **growth, profitability, and risk** to make better investment decisions.")

# ----------------------
# Sidebar
# ----------------------
st.sidebar.header("Settings")

company_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"]
selected_companies = st.sidebar.multiselect(
    "Select Companies", company_options, default=["AAPL", "MSFT", "GOOGL"]
)

years_range = st.sidebar.slider("Select Year Range", 2018, 2024, (2020, 2024))

risk_profile = st.sidebar.selectbox(
    "Investor Profile",
    ["Conservative", "Balanced", "Aggressive"]
)

# ----------------------
# Data fetching
# ----------------------
@st.cache_data(ttl=3600)
def get_data(ticker, start_year):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=f"{start_year}-01-01")
    info = stock.info

    return hist, {
        "Market Cap": info.get("marketCap"),
        "P/E": info.get("trailingPE"),
        "ROE": info.get("returnOnEquity"),
        "Net Margin": info.get("profitMargins"),
        "Debt to Equity": info.get("debtToEquity"),
    }

# ----------------------
# Load data
# ----------------------
data_dict = {}
rows = []

with st.spinner("Fetching financial data..."):
    for company in selected_companies:
        hist, metrics = get_data(company, years_range[0])
        data_dict[company] = hist

        row = {"Company": company}
        row.update(metrics)
        rows.append(row)

metrics_df = pd.DataFrame(rows)

# ----------------------
# Data cleaning
# ----------------------
for col in ["P/E", "ROE", "Net Margin", "Debt to Equity"]:
    metrics_df[col] = pd.to_numeric(metrics_df[col], errors="coerce")

# ----------------------
# Calculate CAGR & Volatility
# ----------------------
cagr_list = []
volatility_list = []

filtered_data = {}

for company, df in data_dict.items():
    df_filtered = df[
        (df.index.year >= years_range[0]) &
        (df.index.year <= years_range[1])
    ]

    filtered_data[company] = df_filtered

    if len(df_filtered) < 2:
        cagr_list.append(np.nan)
        volatility_list.append(np.nan)
        continue

    start_price = df_filtered["Close"].iloc[0]
    end_price = df_filtered["Close"].iloc[-1]

    years = years_range[1] - years_range[0]
    if start_price > 0 and years > 0:
        cagr = (end_price / start_price) ** (1 / years) - 1
    else:
        cagr = np.nan

    returns = df_filtered["Close"].pct_change()
    volatility = returns.std()

    cagr_list.append(cagr)
    volatility_list.append(volatility)

metrics_df["CAGR"] = cagr_list
metrics_df["Volatility"] = volatility_list

# ----------------------
# Scoring system
# ----------------------
metrics_df["growth_score"] = metrics_df["CAGR"].rank(pct=True)

metrics_df["profit_score"] = (
    metrics_df["ROE"].rank(pct=True) +
    metrics_df["Net Margin"].rank(pct=True)
) / 2

metrics_df["risk_score"] = (
    1 - metrics_df["Debt to Equity"].rank(pct=True)
)

# Investor preference weights
if risk_profile == "Conservative":
    w_growth, w_profit, w_risk = 0.2, 0.3, 0.5
elif risk_profile == "Balanced":
    w_growth, w_profit, w_risk = 0.4, 0.3, 0.3
else:
    w_growth, w_profit, w_risk = 0.6, 0.2, 0.2

metrics_df["total_score"] = (
    w_growth * metrics_df["growth_score"] +
    w_profit * metrics_df["profit_score"] +
    w_risk * metrics_df["risk_score"]
)

# ----------------------
# Identify top companies
# ----------------------
top_company = metrics_df.sort_values("total_score", ascending=False).iloc[0]["Company"]
top_growth = metrics_df.sort_values("CAGR", ascending=False).iloc[0]["Company"]
top_profit = metrics_df.sort_values("profit_score", ascending=False).iloc[0]["Company"]
lowest_risk = metrics_df.sort_values("risk_score", ascending=False).iloc[0]["Company"]

# ----------------------
# KPI cards
# ----------------------
st.subheader("🏆 Key Insights")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Best Overall", top_company)
col2.metric("Best Growth", top_growth)
col3.metric("Best Profitability", top_profit)
col4.metric("Lowest Risk", lowest_risk)

# ----------------------
# Price trend
# ----------------------
st.subheader("📈 Stock Price Trend")

fig = px.line()

for company, df in filtered_data.items():
    if not df.empty:
        fig.add_scatter(x=df.index, y=df["Close"], mode="lines", name=company)

fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Score comparison
# ----------------------
st.subheader("📊 Investment Score Comparison")

fig2 = px.bar(
    metrics_df,
    x="Company",
    y="total_score",
    color="Company",
    text="total_score"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------
# Data table
# ----------------------
st.subheader("📋 Financial Metrics")

st.dataframe(
    metrics_df.set_index("Company").style.format({
        "CAGR": "{:.2%}",
        "ROE": "{:.2%}",
        "Net Margin": "{:.2%}",
        "Volatility": "{:.4f}",
        "total_score": "{:.2f}"
    }),
    use_container_width=True
)

# ----------------------
# Final recommendation
# ----------------------
st.subheader("💡 Investment Recommendation")

st.success(f"""
Based on your selected profile (**{risk_profile}**),  
**{top_company}** is the best investment choice.

### Why?
- Strong growth performance (CAGR)
- Solid profitability (ROE & Net Margin)
- Acceptable risk level

This makes it the most balanced option among selected companies.
""")

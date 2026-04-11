# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 页面设置
st.set_page_config(page_title="Tech Giants Financial Comparison", layout="wide")

# 标题
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Tech Giants Financial Comparison Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Compare financial indicators of top global tech companies. Ideal for investors or business students.</p>", unsafe_allow_html=True)

# ----------------------
# Sidebar input
# ----------------------
st.sidebar.header("Settings")
company_options = ["AAPL", "MSFT", "GOOGL"]
selected_companies = st.sidebar.multiselect("Select Companies", company_options, default=company_options)

years_range = st.sidebar.slider("Select Year Range", 2018, 2023, (2020, 2023))

metric_options = ["Market Cap", "P/E", "ROE", "Gross Margin", "Net Margin", "Debt to Equity"]
selected_metric = st.sidebar.selectbox("Select Financial Metric", metric_options)

# ----------------------
# Data fetching
# ----------------------
@st.cache_data
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max")
    info = stock.info
    metrics = {
        "Market Cap": info.get("marketCap"),
        "P/E": info.get("trailingPE"),
        "ROE": info.get("returnOnEquity"),
        "Gross Margin": info.get("grossMargins"),
        "Net Margin": info.get("profitMargins"),
        "Debt to Equity": info.get("debtToEquity")
    }
    return hist, metrics

data_dict = {}
metrics_df = pd.DataFrame(columns=["Company"] + metric_options)

for company in selected_companies:
    hist, metrics = get_financial_data(company)
    data_dict[company] = hist
    row = {"Company": company}
    row.update(metrics)
    metrics_df = pd.concat([metrics_df, pd.DataFrame([row])], ignore_index=True)

# ----------------------
# Stock price trend
# ----------------------
st.markdown("<h2 style='text-align:center; color: #1E90FF;'>Stock Price Trend</h2>", unsafe_allow_html=True)
if selected_companies:
    fig = px.line()
    for company in selected_companies:
        df = data_dict[company]
        df_filtered = df[(df.index.year >= years_range[0]) & (df.index.year <= years_range[1])]
        fig.add_scatter(x=df_filtered.index, y=df_filtered["Close"], mode="lines", name=company)
    fig.update_layout(title="Stock Price Trend", xaxis_title="Date", yaxis_title="Close Price (USD)", legend_title="Company", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Financial metric comparison
# ----------------------
st.markdown(f"<h2 style='text-align:center; color: #1E90FF;'>{selected_metric} Comparison</h2>", unsafe_allow_html=True)
if not metrics_df.empty:
    fig2 = px.bar(metrics_df, x="Company", y=selected_metric, text=selected_metric, color="Company", color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(title=f"{selected_metric} Comparison", yaxis_title=selected_metric, template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------
# Data table
# ----------------------
st.markdown("<h2 style='text-align:center; color: #1E90FF;'>Financial Metrics Table</h2>", unsafe_allow_html=True)
st.dataframe(metrics_df.set_index("Company"), use_container_width=True)

# ----------------------
# Automated financial analysis with cards
# ----------------------
st.markdown("<h2 style='text-align:center; color: #1E90FF;'>Automated Financial Analysis</h2>", unsafe_allow_html=True)
if not metrics_df.empty:
    try:
        # Numeric conversion
        metrics_df[selected_metric] = pd.to_numeric(metrics_df[selected_metric], errors='coerce')
        metrics_df["Net Margin"] = pd.to_numeric(metrics_df["Net Margin"], errors='coerce')
        metrics_df["ROE"] = pd.to_numeric(metrics_df["ROE"], errors='coerce')
        metrics_df["Debt to Equity"] = pd.to_numeric(metrics_df["Debt to Equity"], errors='coerce')
        metrics_df["P/E"] = pd.to_numeric(metrics_df["P/E"], errors='coerce')

        # Profitability card
        top_profit_idx = metrics_df[["Net Margin","ROE"]].mean(axis=1).idxmax()
        top_profit_company = metrics_df.loc[top_profit_idx,"Company"]
        st.markdown(f"<div style='border:1px solid #1E90FF; padding:10px; border-radius:5px; background-color:#F0F8FF;'>"
                    f"<h4>Profitability Analysis</h4>"
                    f"<p>Based on <b>Net Margin</b> and <b>ROE</b>, <b>{top_profit_company}</b> demonstrates the strongest profitability among the selected companies, indicating efficient management and good cost control.</p>"
                    f"</div>", unsafe_allow_html=True)

        # Growth card
        price_start = {}
        price_end = {}
        for company in selected_companies:
            df = data_dict[company]
            df_filtered = df[(df.index.year >= years_range[0]) & (df.index.year <= years_range[1])]
            price_start[company] = df_filtered["Close"].iloc[0]
            price_end[company] = df_filtered["Close"].iloc[-1]
        growth_rate = {c: (price_end[c]-price_start[c])/price_start[c]*100 for c in selected_companies}
        top_growth = max(growth_rate, key=growth_rate.get)
        st.markdown(f"<div style='border:1px solid #32CD32; padding:10px; border-radius:5px; background-color:#F0FFF0;'>"
                    f"<h4>Growth Analysis</h4>"
                    f"<p>Considering stock price trend over the selected years, <b>{top_growth}</b> shows the highest growth ({growth_rate[top_growth]:.2f}%), reflecting strong market performance and investor confidence.</p>"
                    f"</div>", unsafe_allow_html=True)

        # Risk card
        risk_score = metrics_df["Debt to Equity"] + metrics_df["P/E"]
        safest_idx = risk_score.idxmin()
        safest_company = metrics_df.loc[safest_idx, "Company"]
        st.markdown(f"<div style='border:1px solid #FF4500; padding:10px; border-radius:5px; background-color:#FFF5F0;'>"
                    f"<h4>Risk Analysis</h4>"
                    f"<p>With relatively low <b>Debt to Equity</b> and <b>P/E</b>, <b>{safest_company}</b> presents the lowest financial risk compared to peers, making it more resilient to market fluctuations.</p>"
                    f"</div>", unsafe_allow_html=True)

    except Exception as e:
        st.write("Error generating analysis:", e)
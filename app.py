import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# Page Config
# ----------------------
st.set_page_config(page_title="WRDS Stock Analyzer", layout="wide")

st.title("📊 WRDS Tech Stock Analyzer")
st.markdown("Risk-adjusted stock analysis using WRDS CRSP dataset.")

# ----------------------
# Sidebar
# ----------------------
st.sidebar.header("Investor Settings")

profile = st.sidebar.selectbox(
    "Investor Profile",
    ["Conservative", "Balanced", "Aggressive"]
)

# ----------------------
# Load Data (IMPORTANT)
# ----------------------
df = pd.read_csv("wrds_results.csv")

# ----------------------
# Data Check
# ----------------------
if df is None or df.empty:
    st.error("Data not found. Please run notebook first to generate wrds_results.csv")
    st.stop()

# ----------------------
# Scoring System
# ----------------------
df["return_score"] = df["Return"].rank(pct=True)
df["risk_score"] = 1 - df["Volatility"].rank(pct=True)
df["sharpe_score"] = df["Sharpe"].rank(pct=True)

if profile == "Conservative":
    w1, w2, w3 = 0.2, 0.5, 0.3
elif profile == "Balanced":
    w1, w2, w3 = 0.3, 0.3, 0.4
else:
    w1, w2, w3 = 0.5, 0.2, 0.3

df["total_score"] = (
    w1 * df["return_score"] +
    w2 * df["risk_score"] +
    w3 * df["sharpe_score"]
)

# ----------------------
# Best Stock
# ----------------------
best_stock = df.sort_values("total_score", ascending=False).iloc[0]["Company"]

# ----------------------
# KPI Section
# ----------------------
st.subheader("📌 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("Best Overall Stock", best_stock)
col2.metric("Highest Return", df.sort_values("Return", ascending=False).iloc[0]["Company"])
col3.metric("Lowest Risk", df.sort_values("Volatility").iloc[0]["Company"])

# ----------------------
# Table
# ----------------------
st.subheader("📋 Financial Metrics (WRDS CRSP)")

st.dataframe(
    df.set_index("Company").style.format({
        "Return": "{:.2%}",
        "Volatility": "{:.2%}",
        "Sharpe": "{:.2f}",
        "total_score": "{:.2f}"
    }),
    use_container_width=True
)

# ----------------------
# Visualization
# ----------------------
st.subheader("📊 Sharpe Ratio Comparison")

fig = px.bar(
    df,
    x="Company",
    y="Sharpe",
    color="Company",
    text="Sharpe"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Recommendation
# ----------------------
st.subheader("💡 Investment Recommendation")

st.success(f"""
Based on WRDS CRSP data analysis:

**{best_stock}** is the optimal investment choice.

This recommendation is based on:
- Higher risk-adjusted return (Sharpe ratio)
- Balanced volatility
- Strong overall performance score
""")

# ----------------------
# Footer
# ----------------------
st.caption("Data Source: WRDS CRSP | Educational Use Only")

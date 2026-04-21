import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="WRDS Tech Stock Analyzer", layout="wide")

st.title("📊 WRDS-Based Tech Stock Analyzer")
st.markdown("Analyze tech stocks using **CRSP data from WRDS** with risk-adjusted metrics.")

# ----------------------
# Sidebar
# ----------------------
st.sidebar.header("Settings")

use_wrds = st.sidebar.checkbox("Use Live WRDS Data", value=True)

risk_profile = st.sidebar.selectbox(
    "Investor Profile",
    ["Conservative", "Balanced", "Aggressive"]
)

# ----------------------
# WRDS Data Function
# ----------------------
@st.cache_data(ttl=3600)
def load_wrds_data():
    try:
        import wrds
        db = wrds.Connection()

        query = """
        SELECT date, permno, ret
        FROM crsp.dsf
        WHERE permno IN (14593, 10107, 84788)
        AND date >= '2020-01-01'
        """

        df = db.raw_sql(query)

        df['ret'] = pd.to_numeric(df['ret'], errors='coerce')

        results = []

        for permno in df['permno'].unique():
            sub = df[df['permno'] == permno]

            ann_return = sub['ret'].mean() * 252
            volatility = sub['ret'].std() * np.sqrt(252)

            sharpe = ann_return / volatility if volatility != 0 else np.nan

            results.append({
                "permno": permno,
                "Return": ann_return,
                "Volatility": volatility,
                "Sharpe": sharpe
            })

        result_df = pd.DataFrame(results)

        mapping = {
            14593: "AAPL",
            10107: "MSFT",
            84788: "GOOGL"
        }

        result_df["Company"] = result_df["permno"].map(mapping)

        return result_df

    except:
        st.warning("WRDS connection failed. Using local fallback data.")
        return pd.read_csv("wrds_results.csv")

# ----------------------
# Load Data
# ----------------------
if use_wrds:
    df = load_wrds_data()
else:
    df = pd.read_csv("wrds_results.csv")

# ----------------------
# Scoring Model
# ----------------------
df["return_score"] = df["Return"].rank(pct=True)
df["risk_score"] = 1 - df["Volatility"].rank(pct=True)
df["sharpe_score"] = df["Sharpe"].rank(pct=True)

if risk_profile == "Conservative":
    w_return, w_risk, w_sharpe = 0.2, 0.5, 0.3
elif risk_profile == "Balanced":
    w_return, w_risk, w_sharpe = 0.3, 0.3, 0.4
else:
    w_return, w_risk, w_sharpe = 0.5, 0.2, 0.3

df["total_score"] = (
    w_return * df["return_score"] +
    w_risk * df["risk_score"] +
    w_sharpe * df["sharpe_score"]
)

# ----------------------
# KPI
# ----------------------
top_company = df.sort_values("total_score", ascending=False).iloc[0]["Company"]

st.subheader("🏆 Investment Insight")

col1, col2, col3 = st.columns(3)

col1.metric("Best Overall", top_company)
col2.metric("Highest Return", df.sort_values("Return", ascending=False).iloc[0]["Company"])
col3.metric("Lowest Risk", df.sort_values("Volatility").iloc[0]["Company"])

# ----------------------
# Table
# ----------------------
st.subheader("📋 WRDS Metrics")

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
# Chart
# ----------------------
st.subheader("📊 Sharpe Ratio Comparison")

fig = px.bar(df, x="Company", y="Sharpe", color="Company", text="Sharpe")
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Recommendation
# ----------------------
st.subheader("💡 Final Recommendation")

st.success(f"""
Based on WRDS CRSP data, **{top_company}** is the best investment choice.

This decision is based on:
- Annualized return
- Volatility (risk)
- Sharpe ratio (risk-adjusted return)

Sharpe ratio is widely used in financial research to evaluate investment performance.
""")

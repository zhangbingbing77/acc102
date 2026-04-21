import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tech Stock Analyzer", layout="wide")

st.title("📊 WRDS Tech Stock Risk Analyzer")

# -----------------------------
# Mock/Preprocessed Data (from notebook)
# -----------------------------
@st.cache_data
def load_data():
    data = {
        "Company": ["AAPL", "MSFT", "GOOGL"],
        "Return": [0.18, 0.15, 0.12],
        "Volatility": [0.22, 0.18, 0.20],
        "Sharpe": [0.82, 0.83, 0.60]
    }
    return pd.DataFrame(data)

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
company = st.sidebar.multiselect(
    "Select Companies",
    df["Company"].tolist(),
    default=df["Company"].tolist()
)

metric = st.sidebar.selectbox(
    "Select Metric",
    ["Return", "Volatility", "Sharpe"]
)

filtered = df[df["Company"].isin(company)]

# -----------------------------
# Chart
# -----------------------------
st.subheader(f"{metric} Comparison")

fig = px.bar(
    filtered,
    x="Company",
    y=metric,
    color="Company",
    text=metric
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Table
# -----------------------------
st.subheader("Financial Metrics Table")
st.dataframe(filtered)

# -----------------------------
# Insight
# -----------------------------
st.subheader("Automated Insight")

best = filtered.loc[filtered["Sharpe"].idxmax(), "Company"]

st.success(f"The best risk-adjusted performer is {best} based on Sharpe Ratio.")

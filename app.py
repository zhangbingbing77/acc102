import streamlit as st
import wrds
import pandas as pd
import plotly.express as px

# ----------------------
# Page config
# ----------------------
st.set_page_config(page_title="WRDS Stock Analyzer", layout="wide")

st.title("📊 WRDS Live Stock Analyzer")
st.markdown("On-demand financial analysis using WRDS CRSP dataset.")

# ----------------------
# Cache WRDS connection (VERY IMPORTANT)
# ----------------------
@st.cache_resource
def connect_wrds():
    return wrds.Connection()

db = connect_wrds()

# ----------------------
# User input (on-demand request)
# ----------------------
st.sidebar.header("Data Query Settings")

permno_dict = {
    "AAPL": 14593,
    "MSFT": 10107,
    "GOOGL": 84788
}

selected_company = st.sidebar.selectbox(
    "Select Company",
    list(permno_dict.keys())
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))

# ----------------------
# Fetch data ONLY when requested
# ----------------------
if st.sidebar.button("Load WRDS Data"):

    permno = permno_dict[selected_company]

    query = f"""
    SELECT date, ret
    FROM crsp.dsf
    WHERE permno = {permno}
    AND date >= '{start_date}'
    ORDER BY date
    LIMIT 1000
    """

    df = db.raw_sql(query)

    # ----------------------
    # Data cleaning
    # ----------------------
    df["ret"] = pd.to_numeric(df["ret"], errors="coerce")
    df = df.dropna()

    # ----------------------
    # Metrics
    # ----------------------
    ann_return = df["ret"].mean() * 252
    volatility = df["ret"].std() * (252 ** 0.5)
    sharpe = ann_return / volatility if volatility != 0 else 0

    # ----------------------
    # Display KPIs
    # ----------------------
    st.subheader(f"📌 Results for {selected_company}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Annual Return", f"{ann_return:.2%}")
    col2.metric("Volatility", f"{volatility:.2%}")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

    # ----------------------
    # Chart
    # ----------------------
    st.subheader("📈 Daily Returns")

    fig = px.line(df, x="date", y="ret", title="Daily Returns Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # ----------------------
    # Insight
    # ----------------------
    st.success(f"""
    Based on WRDS CRSP data:

    {selected_company} shows:
    - Risk-adjusted performance (Sharpe): {sharpe:.2f}
    - Moderate volatility: {volatility:.2%}

    This indicates a balance between risk and return.
    """)

# ----------------------
# Footer
# ----------------------
st.caption("Data Source: WRDS CRSP | On-demand query model | Educational use only")

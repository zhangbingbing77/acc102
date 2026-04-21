# 📊 WRDS Live Stock Analyzer (Data Product Project)

## Course Information
ACC102 Data Product  
Xi’an Jiaotong-Liverpool University  
2024–2025 Semester 2  

---

## 👤 Student Information
- Name: YOUR NAME  
- Student ID: YOUR ID  
- Track: Track 4 – Interactive Data Analysis Tool  
- Project Type: Streamlit Data Product  

---

# 🎯 1. Project Overview

This project is an interactive financial data analysis tool built using Python and Streamlit.

It allows users to dynamically retrieve and analyze stock performance data from the WRDS CRSP database.

The tool focuses on evaluating risk-adjusted returns of major technology stocks using financial metrics such as:

- Annualized Return  
- Volatility  
- Sharpe Ratio  

---

# ❓ 2. Research Question

Which technology stock provides the best risk-adjusted return based on WRDS CRSP historical data?

---

# 📊 3. Data Source

- Source: WRDS (CRSP Daily Stock File)
- Type: Financial market data (daily returns)
- Access Method: Python WRDS API (on-demand query)
- Data Retrieval Date: April 2026

---

# ⚙️ 4. Data Pipeline

This project follows a two-stage workflow:

### Step 1: Data Collection
- Data is retrieved directly from WRDS CRSP database
- Users select a stock and time range in the Streamlit interface
- Data is fetched on demand (not pre-stored)

### Step 2: Data Processing
- Calculation of:
  - Annualized Return
  - Volatility
  - Sharpe Ratio
- Results displayed interactively in Streamlit

---

# 🧠 5. Methodology

The following financial metrics are used:

### Annualized Return
Measures long-term growth of the stock.

### Volatility
Measures the risk level based on return fluctuations.

### Sharpe Ratio
Measures risk-adjusted performance:

Sharpe = Return / Volatility

A higher Sharpe Ratio indicates better performance per unit of risk.

---

# 🛠️ 6. Tools & Technologies

- Python
- Streamlit
- WRDS (CRSP Database)
- Pandas
- Plotly

---

# 📈 7. Features

- Interactive stock selection
- On-demand WRDS data retrieval
- Real-time financial metric calculation
- Visualized return trends
- Risk-return analysis dashboard

---

# ⚠️ 8. Important Notes (Compliance)

- No manually created or hardcoded financial datasets are used.
- All data is retrieved directly from WRDS upon user request.
- The application does not rely on external CSV or Excel files.
- Data is not pre-stored to ensure compliance with Track 4 requirements.

---

# 🚧 9. Limitations

- Limited number of stocks available in the demo
- Performance depends on WRDS server response time
- Only historical data is considered (no real-time trading signals)
- No macroeconomic variables included

---

# 💡 10. Future Improvements

- Expand stock universe
- Add portfolio optimization module
- Include macroeconomic indicators
- Improve caching and performance optimization

---

# 📌 11. How to Run the Project

1. Install dependencies:

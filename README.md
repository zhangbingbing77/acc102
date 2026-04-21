# 📊 WRDS Live Stock Analyzer (Data Product Project)

## 👤 Student Information
- Name: Bingbing Zhang  
- Student ID: 2469540 
- Project Type: Streamlit Interactive Data Product  
- Track 4 – Interactive Data Analysis Tool 
---

# 1. Problem Definition

This project aims to analyze and compare the risk-adjusted performance of major technology stocks using historical market data from WRDS.

The core problem is to identify which stock provides the best balance between return and risk based on empirical financial data.

The motivation is to move beyond simple return comparison and focus on risk-adjusted investment performance.

---

# 2. Target Users / Audience

The target users of this project include:

- University students studying finance, economics, or data analytics  
- Beginner investors interested in quantitative investment analysis  
- Users who want to understand risk-return trade-offs in financial markets  

The tool is designed for educational and decision-support purposes rather than professional trading.

---

# 3. Dataset Description

Data Source: WRDS (CRSP Daily Stock File)  
Access Method: Python WRDS API (on-demand SQL query)  
Data Retrieval Date: April 2026  

Variables:
- date: trading date  
- ret: daily stock return  
- permno: stock identifier  

All data is retrieved dynamically upon request. No pre-stored datasets are used.

---

# 4. Methodology

Step 1: Data is retrieved from WRDS CRSP database using SQL queries.  
Step 2: Data is cleaned and converted into numeric format.  
Step 3: Financial indicators are calculated:

- Annualized Return = mean(daily return) × 252  
- Volatility = standard deviation × √252  
- Sharpe Ratio = Return / Volatility  

Step 4: Stocks are compared based on risk-adjusted performance.

---

# 5. Key Insights

The analysis shows that stocks differ significantly in both return and risk levels.

- High return stocks often come with higher volatility  
- Stable stocks may offer lower returns  
- Sharpe Ratio provides a balanced performance measure  

Overall, the best stock is not the one with highest return, but highest risk-adjusted efficiency.

---

# 6. How to Run the Project

Step 1: Install dependencies  
pip install streamlit wrds pandas plotly  

Step 2: Run the app  
streamlit run app.py  

Step 3: Use the app  
- Select stock from sidebar  
- Choose time range  
- Click load data  
- View charts and metrics  

Data is not stored locally. All data is fetched from WRDS.

# 📦 Project Structure

/project  
│── app.py  
│── README.md  
│── notebook.ipynb (WRDS analysis process)
